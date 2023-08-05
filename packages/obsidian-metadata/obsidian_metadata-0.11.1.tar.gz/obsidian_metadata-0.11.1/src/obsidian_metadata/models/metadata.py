"""Work with metadata items."""

import copy
import re
from io import StringIO

from rich.columns import Columns
from rich.table import Table
from ruamel.yaml import YAML

from obsidian_metadata._utils import (
    clean_dictionary,
    delete_from_dict,
    dict_contains,
    dict_values_to_lists_strings,
    inline_metadata_from_string,
    merge_dictionaries,
    remove_markdown_sections,
    rename_in_dict,
)
from obsidian_metadata._utils.alerts import logger as log
from obsidian_metadata._utils.console import console
from obsidian_metadata.models import Patterns  # isort: ignore
from obsidian_metadata.models.enums import MetadataType
from obsidian_metadata.models.exceptions import (
    FrontmatterError,
    InlineMetadataError,
    InlineTagError,
)

PATTERNS = Patterns()
INLINE_TAG_KEY: str = "inline_tag"


class VaultMetadata:
    """Representation of all Metadata in the Vault.

    Attributes:
        dict (dict): Dictionary of all frontmatter and inline metadata. Does not include tags.
        frontmatter (dict): Dictionary of all frontmatter metadata.
        inline_metadata (dict): Dictionary of all inline metadata.
        tags (list): List of all tags.
    """

    def __init__(self) -> None:
        self.dict: dict[str, list[str]] = {}
        self.frontmatter: dict[str, list[str]] = {}
        self.inline_metadata: dict[str, list[str]] = {}
        self.tags: list[str] = []

    def __repr__(self) -> str:
        """Representation of all metadata."""
        return str(self.dict)

    def index_metadata(
        self, area: MetadataType, metadata: dict[str, list[str]] | list[str]
    ) -> None:
        """Index pre-existing metadata in the vault. Takes a dictionary as input and merges it with the existing metadata.  Does not overwrite existing keys.

        Args:
            area (MetadataType): Type of metadata.
            metadata (dict): Metadata to add.
        """
        if isinstance(metadata, dict):
            new_metadata = clean_dictionary(metadata)
            self.dict = merge_dictionaries(self.dict, new_metadata)

        if area == MetadataType.FRONTMATTER:
            self.frontmatter = merge_dictionaries(self.frontmatter, new_metadata)

        if area == MetadataType.INLINE:
            self.inline_metadata = merge_dictionaries(self.inline_metadata, new_metadata)

        if area == MetadataType.TAGS and isinstance(metadata, list):
            self.tags.extend(metadata)
            self.tags = sorted({s.strip("#") for s in self.tags})

    def contains(
        self, area: MetadataType, key: str = None, value: str = None, is_regex: bool = False
    ) -> bool:
        """Check if a key and/or a value exists in the metadata.

        Args:
            area (MetadataType): Type of metadata to check.
            key (str, optional): Key to check.
            value (str, optional): Value to check.
            is_regex (bool, optional): Use regex to check. Defaults to False.

        Returns:
            bool: True if the key exists.

        Raises:
            ValueError: Key must be provided when checking for a key's existence.
            ValueError: Value must be provided when checking for a tag's existence.
        """
        if area != MetadataType.TAGS and key is None:
            raise ValueError("Key must be provided when checking for a key's existence.")

        match area:
            case MetadataType.ALL:
                return dict_contains(self.dict, key, value, is_regex)
            case MetadataType.FRONTMATTER:
                return dict_contains(self.frontmatter, key, value, is_regex)
            case MetadataType.INLINE:
                return dict_contains(self.inline_metadata, key, value, is_regex)
            case MetadataType.KEYS:
                return dict_contains(self.dict, key, value, is_regex)
            case MetadataType.TAGS:
                if value is None:
                    raise ValueError("Value must be provided when checking for a tag's existence.")
                if is_regex:
                    return any(re.search(value, tag) for tag in self.tags)
                return value in self.tags

    def delete(self, key: str, value_to_delete: str = None) -> bool:
        """Delete a key or a value from the VaultMetadata dict object. Regex is supported to allow deleting more than one key or value.

        Args:
            key (str): Key to check.
            value_to_delete (str, optional): Value to delete.

        Returns:
            bool: True if a value was deleted
        """
        new_dict = delete_from_dict(
            dictionary=self.dict,
            key=key,
            value=value_to_delete,
            is_regex=True,
        )

        if new_dict != self.dict:
            self.dict = dict(new_dict)
            return True

        return False

    def print_metadata(self, area: MetadataType) -> None:
        """Print metadata to the terminal.

        Args:
            area (MetadataType): Type of metadata to print
        """
        dict_to_print = None
        list_to_print = None
        match area:
            case MetadataType.INLINE:
                dict_to_print = self.inline_metadata
                header = "All inline metadata"
            case MetadataType.FRONTMATTER:
                dict_to_print = self.frontmatter
                header = "All frontmatter"
            case MetadataType.TAGS:
                list_to_print = [f"#{x}" for x in self.tags]
                header = "All inline tags"
            case MetadataType.KEYS:
                list_to_print = sorted(self.dict.keys())
                header = "All Keys"
            case MetadataType.ALL:
                dict_to_print = self.dict
                list_to_print = [f"#{x}" for x in self.tags]
                header = "All metadata"

        if dict_to_print is not None:
            table = Table(title=header, show_footer=False, show_lines=True)
            table.add_column("Keys")
            table.add_column("Values")
            for key, value in sorted(dict_to_print.items()):
                values: str | dict[str, list[str]] = (
                    "\n".join(sorted(value)) if isinstance(value, list) else value
                )
                table.add_row(f"[bold]{key}[/]", str(values))
            console.print(table)

        if list_to_print is not None:
            columns = Columns(
                sorted(list_to_print),
                equal=True,
                expand=True,
                title=header if area != MetadataType.ALL else "All inline tags",
            )
            console.print(columns)

    def rename(self, key: str, value_1: str, value_2: str = None) -> bool:
        """Replace a value in the frontmatter.

        Args:
            key (str): Key to check.
            value_1 (str): `With value_2` this is the value to rename. If `value_2` is None this is the renamed key
            value_2 (str, Optional): New value.

        Returns:
            bool: True if a value was renamed
        """
        new_dict = rename_in_dict(dictionary=self.dict, key=key, value_1=value_1, value_2=value_2)

        if new_dict != self.dict:
            self.dict = dict(new_dict)
            return True

        return False


class Frontmatter:
    """Representation of frontmatter metadata."""

    def __init__(self, file_content: str) -> None:
        self.dict: dict[str, list[str]] = self._grab_note_frontmatter(file_content)
        self.dict_original: dict[str, list[str]] = copy.deepcopy(self.dict)

    def __repr__(self) -> str:  # pragma: no cover
        """Representation of the frontmatter.

        Returns:
            str: frontmatter
        """
        return f"Frontmatter(frontmatter={self.dict})"

    def _grab_note_frontmatter(self, file_content: str) -> dict:
        """Grab metadata from a note.

        Args:
            file_content (str): Content of the note.

        Returns:
            dict: Metadata from the note.
        """
        try:
            frontmatter_block: str = PATTERNS.frontmatt_block_strip_separators.search(
                file_content
            ).group("frontmatter")
        except AttributeError:
            return {}

        yaml = YAML(typ="safe")
        yaml.allow_unicode = False
        try:
            frontmatter: dict = yaml.load(frontmatter_block)
        except Exception as e:  # noqa: BLE001
            raise FrontmatterError(e) from e

        if frontmatter is None or frontmatter == [None]:
            return {}

        for k in frontmatter:
            if frontmatter[k] is None:
                frontmatter[k] = []

        return dict_values_to_lists_strings(frontmatter, strip_null_values=True)

    def add(self, key: str, value: str | list[str] = None) -> bool:  # noqa: PLR0911
        """Add a key and value to the frontmatter.

        Args:
            key (str): Key to add.
            value (str, optional): Value to add.

        Returns:
            bool: True if the metadata was added
        """
        if value is None:
            if key not in self.dict:
                self.dict[key] = []
                return True
            return False

        if key not in self.dict:
            if isinstance(value, list):
                self.dict[key] = value
                return True

            self.dict[key] = [value]
            return True

        if key in self.dict and value not in self.dict[key]:
            if isinstance(value, list):
                self.dict[key].extend(value)
                self.dict[key] = list(sorted(set(self.dict[key])))
                return True

            self.dict[key].append(value)
            return True

        return False

    def contains(self, key: str, value: str = None, is_regex: bool = False) -> bool:
        """Check if a key or value exists in the metadata.

        Args:
            key (str): Key to check.
            value (str, optional): Value to check.
            is_regex (bool, optional): Use regex to check. Defaults to False.

        Returns:
            bool: True if the key exists.
        """
        return dict_contains(self.dict, key, value, is_regex)

    def delete(self, key: str, value_to_delete: str = None, is_regex: bool = False) -> bool:
        """Delete a value or key in the frontmatter.  Regex is supported to allow deleting more than one key or value.

        Args:
            is_regex (bool, optional): Use regex to check. Defaults to False.
            key (str): If no value, key to delete. If value, key containing the value.
            value_to_delete (str, optional): Value to delete.

        Returns:
            bool: True if a value was deleted
        """
        new_dict = delete_from_dict(
            dictionary=self.dict,
            key=key,
            value=value_to_delete,
            is_regex=is_regex,
        )

        if new_dict != self.dict:
            self.dict = dict(new_dict)
            return True

        return False

    def delete_all(self) -> None:
        """Delete all Frontmatter from the note."""
        self.dict = {}

    def has_changes(self) -> bool:
        """Check if the frontmatter has changes.

        Returns:
            bool: True if the frontmatter has changes.
        """
        return self.dict != self.dict_original

    def rename(self, key: str, value_1: str, value_2: str = None) -> bool:
        """Replace a value in the frontmatter.

        Args:
            key (str): Key to check.
            value_1 (str): `With value_2` this is the value to rename. If `value_2` is None this is the renamed key
            value_2 (str, Optional): New value.

        Returns:
            bool: True if a value was renamed
        """
        new_dict = rename_in_dict(dictionary=self.dict, key=key, value_1=value_1, value_2=value_2)

        if new_dict != self.dict:
            self.dict = dict(new_dict)
            return True

        return False

    def to_yaml(self, sort_keys: bool = False) -> str:
        """Return the frontmatter as a YAML string.

        Returns:
            str: Frontmatter as a YAML string.
            sort_keys (bool, optional): Sort the keys. Defaults to False.
        """
        dict_to_dump = copy.deepcopy(self.dict)
        for k in dict_to_dump:
            if dict_to_dump[k] == []:
                dict_to_dump[k] = None
            if isinstance(dict_to_dump[k], list) and len(dict_to_dump[k]) == 1:
                new_val = dict_to_dump[k][0]
                dict_to_dump[k] = new_val  # type: ignore [assignment]

        # Converting stream to string from https://stackoverflow.com/questions/47614862/best-way-to-use-ruamel-yaml-to-dump-yaml-to-string-not-to-stream/63179923#63179923

        if sort_keys:
            dict_to_dump = dict(sorted(dict_to_dump.items()))

        yaml = YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
        string_stream = StringIO()
        yaml.dump(dict_to_dump, string_stream)
        yaml_value = string_stream.getvalue()
        string_stream.close()
        return yaml_value


class InlineMetadata:
    """Representation of inline metadata in the form of `key:: value`."""

    def __init__(self, file_content: str) -> None:
        self.dict: dict[str, list[str]] = self._grab_inline_metadata(file_content)
        self.dict_original: dict[str, list[str]] = copy.deepcopy(self.dict)

    def __repr__(self) -> str:  # pragma: no cover
        """Representation of inline metadata.

        Returns:
            str: inline metadata
        """
        return f"InlineMetadata(inline_metadata={self.dict})"

    def _grab_inline_metadata(self, file_content: str) -> dict[str, list[str]]:
        """Grab inline metadata from a note.

        Returns:
            dict[str, str]: Inline metadata from the note.
        """
        content = remove_markdown_sections(
            file_content,
            strip_codeblocks=True,
            strip_inlinecode=True,
            strip_frontmatter=True,
        )
        found_inline_metadata = inline_metadata_from_string(content)
        inline_metadata: dict[str, list[str]] = {}

        try:
            for k, v in found_inline_metadata:
                if not k:
                    log.trace(f"Skipping empty key associated with value: {v}")
                    continue
                if k in inline_metadata:
                    inline_metadata[k].append(str(v))
                else:
                    inline_metadata[k] = [str(v)]
        except ValueError as e:
            raise InlineMetadataError(
                f"Error parsing inline metadata: {found_inline_metadata}"
            ) from e
        except AttributeError as e:
            raise InlineMetadataError(
                f"Error parsing inline metadata: {found_inline_metadata}"
            ) from e

        return clean_dictionary(inline_metadata)

    def add(self, key: str, value: str | list[str] = None) -> bool:  # noqa: PLR0911
        """Add a key and value to the inline metadata.

        Args:
            key (str): Key to add.
            value (str, optional): Value to add.

        Returns:
            bool: True if the metadata was added
        """
        if value is None:
            if key not in self.dict:
                self.dict[key] = []
                return True
            return False

        if key not in self.dict:
            if isinstance(value, list):
                self.dict[key] = value
                return True

            self.dict[key] = [value]
            return True

        if key in self.dict and value not in self.dict[key]:
            if isinstance(value, list):
                self.dict[key].extend(value)
                self.dict[key] = list(sorted(set(self.dict[key])))
                return True

            self.dict[key].append(value)
            return True

        return False

    def contains(self, key: str, value: str = None, is_regex: bool = False) -> bool:
        """Check if a key or value exists in the inline metadata.

        Args:
            key (str): Key to check.
            value (str, Optional): Value to check.
            is_regex (bool, optional): If True, key and value are treated as regex. Defaults to False.

        Returns:
            bool: True if the key exists.
        """
        return dict_contains(self.dict, key, value, is_regex)

    def delete(self, key: str, value_to_delete: str = None, is_regex: bool = False) -> bool:
        """Delete a value or key in the inline metadata. Regex is supported to allow deleting more than one key or value.

        Args:
            is_regex (bool, optional): If True, key and value are treated as regex. Defaults to False.
            key (str): If no value, key to delete. If value, key containing the value.
            value_to_delete (str, optional): Value to delete.

        Returns:
            bool: True if a value was deleted
        """
        new_dict = delete_from_dict(
            dictionary=self.dict,
            key=key,
            value=value_to_delete,
            is_regex=is_regex,
        )

        if new_dict != self.dict:
            self.dict = dict(new_dict)
            return True

        return False

    def has_changes(self) -> bool:
        """Check if the metadata has changes.

        Returns:
            bool: True if the metadata has changes.
        """
        return self.dict != self.dict_original

    def rename(self, key: str, value_1: str, value_2: str = None) -> bool:
        """Replace a value in the inline metadata.

        Args:
            key (str): Key to check.
            value_1 (str): `With value_2` this is the value to rename. If `value_2` is None this is the renamed key
            value_2 (str, Optional): New value.

        Returns:
            bool: True if a value was renamed
        """
        new_dict = rename_in_dict(dictionary=self.dict, key=key, value_1=value_1, value_2=value_2)

        if new_dict != self.dict:
            self.dict = dict(new_dict)
            return True

        return False


class InlineTags:
    """Representation of inline tags."""

    def __init__(self, file_content: str) -> None:
        self.metadata_key = INLINE_TAG_KEY
        self.list: list[str] = self._grab_inline_tags(file_content)
        self.list_original: list[str] = self.list.copy()

    def __repr__(self) -> str:  # pragma: no cover
        """Representation of the inline tags.

        Returns:
            str: inline tags
        """
        return f"InlineTags(tags={self.list})"

    def _grab_inline_tags(self, file_content: str) -> list[str]:
        """Grab inline tags from a note.

        Args:
            file_content (str): Total contents of the note file (frontmatter and content).

        Returns:
            list[str]: Inline tags from the note.
        """
        try:
            return sorted(
                PATTERNS.find_inline_tags.findall(
                    remove_markdown_sections(
                        file_content,
                        strip_codeblocks=True,
                        strip_inlinecode=True,
                    )
                )
            )
        except AttributeError as e:
            raise InlineTagError("Error parsing inline tags.") from e
        except TypeError as e:
            raise InlineTagError("Error parsing inline tags.") from e
        except ValueError as e:
            raise InlineTagError("Error parsing inline tags.") from e

    def add(self, new_tag: str | list[str]) -> bool:
        """Add a new inline tag.

        Args:
            new_tag (str, list[str]): Tag to add.

        Returns:
            bool: True if a tag was added.
        """
        added_tag = False
        if isinstance(new_tag, list):
            for _tag in new_tag:
                if _tag.startswith("#"):
                    _tag = _tag[1:]
                if _tag in self.list:
                    continue
                self.list.append(_tag)
                added_tag = True

            if added_tag:
                self.list = sorted(self.list)
                return True
            return False

        if new_tag.startswith("#"):
            new_tag = new_tag[1:]
        if new_tag in self.list:
            return False
        new_list = self.list.copy()
        new_list.append(new_tag)
        self.list = sorted(new_list)
        return True

    def contains(self, tag: str, is_regex: bool = False) -> bool:
        """Check if a tag exists in the metadata.

        Args:
            tag (str): Tag to check.
            is_regex (bool, optional): If True, tag is treated as regex. Defaults to False.

        Returns:
            bool: True if the tag exists.
        """
        if is_regex is True:
            return any(re.search(tag, _t) for _t in self.list)

        if tag in self.list:
            return True

        return False

    def delete(self, tag_to_delete: str) -> bool:
        """Delete a specified inline tag. Regex is supported to allow deleting more than one tag.

        Args:
            tag_to_delete (str, optional): Value to delete.

        Returns:
            bool: True if a value was deleted
        """
        new_list = sorted([x for x in self.list if re.search(tag_to_delete, x) is None])

        if new_list != self.list:
            self.list = new_list
            return True
        return False

    def has_changes(self) -> bool:
        """Check if the metadata has changes.

        Returns:
            bool: True if the metadata has changes.
        """
        return self.list != self.list_original

    def rename(self, old_tag: str, new_tag: str) -> bool:
        """Replace an inline tag with another string.

        Args:
            old_tag (str): `With value_2` this is the value to rename.
            new_tag (str): New value

        Returns:
            bool: True if a value was renamed
        """
        if old_tag in self.list and new_tag is not None and new_tag:
            self.list = sorted({new_tag if i == old_tag else i for i in self.list})
            return True
        return False
