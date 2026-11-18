import os

from ScriptCollection.GeneralUtilities import Platform
from ScriptCollection.TFCPS.Docker.TFCPS_CodeUnitSpecific_Docker import TFCPS_CodeUnitSpecific_Docker_Functions,TFCPS_CodeUnitSpecific_Docker_CLI


def build():
    platforms:list[Platform] = [
            Platform.Linux_AMD64,
            Platform.Linux_ARM64,
    ]
    tf:TFCPS_CodeUnitSpecific_Docker_Functions=TFCPS_CodeUnitSpecific_Docker_CLI.parse(__file__)
    resources_folder=os.path.join(tf.get_codeunit_folder(),"Other","Resources")
    def dependency_version(dependency_name:str)->str:
        return tf.tfcps_Tools_General.get_dependency_version_in_resources_folder(resources_folder,dependency_name)
    # each build-arg is read from the corresponding Other/Resources/Dependencies/<dependency>/Version.txt-file
    build_arguments={
        "SambaVersion":dependency_version("Samba"),
    }
    tf.build(platforms,build_arguments)


if __name__ == "__main__":
    build()
