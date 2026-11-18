import re
from ScriptCollection.GeneralUtilities import GeneralUtilities
from ScriptCollection.ScriptCollectionCore import ScriptCollectionCore
from ScriptCollection.TFCPS.Docker.TFCPS_CodeUnitSpecific_Docker import TFCPS_CodeUnitSpecific_Docker_Functions,TFCPS_CodeUnitSpecific_Docker_CLI

class Updater:

    def __init__(self):
        self.__tf: TFCPS_CodeUnitSpecific_Docker_Functions = TFCPS_CodeUnitSpecific_Docker_CLI.parse(__file__)
        self.__sc: ScriptCollectionCore = ScriptCollectionCore()

    def __get_latest_version_of_samba(self) -> str:
        """Returns the version of the apk-package "samba" which the alpine-image of the repository provides.

        The version is asked in exactly the alpine-image which the image is built from (see
        ".ScriptCollection/OCIImages/ImageDefinition.csv"), because an alpine-branch only provides the newest build of a
        package: the pinned version must be the one which this branch provides, otherwise "apk add" fails.
        The version consists of the version of samba and the alpine-specific package-release (for example "4.22.10-r0")
        and not of three numbers, so the echolon can not be applied to it and the provided version is always taken over.
        That is why it is in the ignored dependencies of the codeunit-file and updated by this script itself."""
        alpine_image: str = self.__tf.tfcps_Tools_General.oci_image_manager.get_registry_address_for_image_with_default_tag(self.__tf.get_repository_folder(), "Alpine")
        output = self.__sc.run_program_argsasarray("docker", ["run", "--rm", alpine_image, "sh", "-c", "apk update >/dev/null && apk policy samba"])
        versions: list[str] = []
        for line in GeneralUtilities.string_to_lines(output[1]):
            match = re.match(r"^\s+(\d+\.\d+\.\d+-r\d+):$", line)
            if match is not None:
                versions.append(match.group(1))
        return GeneralUtilities.get_only_item_from_list(versions)

    def update_dependencies(self):
        """Updates the dependencies of this codeunit using the generic dependency-update of ScriptCollection, which also
        informs about newer major-versions which are not taken over."""
        self.__tf.update_dependencies()
        self.__tf.set_dependency_version("Samba", self.__get_latest_version_of_samba())

def update_dependencies():
    updater=Updater()
    updater.update_dependencies()


if __name__ == "__main__":
    update_dependencies()
