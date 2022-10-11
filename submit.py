"""
This script will submit current file to deadline for render
"""
import os
import sys
import subprocess
import json

def job_info(info_txt):
    """
    this function will collect scene file information and write a job file
    :return:
    """
    # renderer_name = 'File'
    # version = cmds.about(version=True)
    # project_path = cmds.workspace(q=True, directory=True)
    # width = cmds.getAttr("defaultResolution.width")
    # height = cmds.getAttr("defaultResolution.height")
    # output_file_path = cmds.workspace(expandName="images")
    # output_file_prefix = cmds.getAttr("defaultRenderGlobals.imageFilePrefix")
    # scene_file = cmds.file(q=True, location=True)


    # Get Command From maya ???
    # info_txt = 'Animation=1\n' \
    #            'Renderer={}\n' \
    #            'UsingRenderLayers=0\n' \
    #            'RenderLayer=\n' \
    #            'RenderHalfFrames=0\n' \
    #            'LocalRendering=0\n' \
    #            'StrictErrorChecking=1\n' \
    #            'MaxProcessors=0\n' \
    #            'AntiAliasing=low\n' \
    #            'Version={}\n' \
    #            'Build=64bit\n' \
    #            'ProjectPath={}\n' \
    #            'ImageWidth={}\n' \
    #            'ImageHeight={}\n' \
    #            'OutputFilePath={}\n' \
    #            'OutputFilePrefix={}\n' \
    #            'Camera=\n' \
    #            'Camera0=\n' \
    #            'Camera1=RENDERShape\n' \
    #            'Camera2=frontShape\n' \
    #            'Camera3=perspShape\n' \
    #            'Camera4=sideShape\n' \
    #            'Camera5=topShape\n' \
    #            'SceneFile={}\n' \
    #            'IgnoreError211=0'.format(renderer_name
    #                                      version,
    #                                      project_path,
    #                                      width,
    #                                      height,
    #                                      output_file_path,
    #                                      output_file_prefix,
    #                                      scene_file)

    job_info_file = r'{}\job_info.job'.format(os.getenv('TEMP'))
    with open(job_info_file, 'w') as job_file:
        job_file.write(info_txt)
    return job_info_file


def plugin_info(info_txt):
    """
    this function will collect maya deadline information and write a job file
    :return:
    """
    # outPutName = ""
    # info_txt = f'Plugin=MayaBatch\n' \
    #            'Name=MY_FILE_NAME\n' \
    #            'Comment=Render Launch by Python\n' \
    #            'Pool=none\n' \
    #            'MachineLimit=0\n' \
    #            'Priority=50\n' \
    #            'OnJobComplete=Nothing\n' \
    #            'TaskTimeoutMinutes=0\n' \
    #            'MinRenderTimeMinutes=0\n' \
    #            'ConcurrentTasks=1\n' \
    #            'Department=\n' \
    #            'Group=none\n' \
    #            'LimitGroups=\n' \
    #            'JobDependencies=\n' \
    #            'InitialStatus=Suspended\n' \
    #            'OutputFilename0={outPutName}\n' \
    #            'Frames=1-10\n' \
    #            'ChunkSize=1'

    plugin_info_file = r'{}\plugin_info.job'.format(os.getenv('TEMP'))
    with open(plugin_info_file, 'w') as job_file:
        job_file.write(info_txt)
    return plugin_info_file


def submit_to_deadline(job_info_txt, plugin_info_txt):
    # Change deadline exe root
    deadline_cmd = r"C:\Program Files\Thinkbox\Deadline10\bin\deadlinecommand.exe"
    job_file = job_info(job_info_txt)
    info_file = plugin_info(plugin_info_txt)
    command = '{deadline_cmd} "{job_file}" "{info_file}"'.format(**vars())
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    lines_iterator = iter(process.stdout.readline, b"")
    #  Lets print the output log to see the Error / Success 
    for line in lines_iterator:
        print(line)
        sys.stdout.flush()

def GetInfoTxtNuke(filePath, frames, chunkSize=1, excuteNodes="REN_EXR", pool="nuke", priority=50, machineLimit=30):
    job_info_txt = f"""
    Frames={frames}
    MachineLimit={machineLimit}
    ChunkSize={chunkSize}
    Group=nuke_13
    Name={os.path.basename(filePath)}
    OverrideTaskExtraInfoNames=False
    Plugin=CommandLine
    Pool={pool}
    Priority={priority}
    ScheduledStartDateTime=15/09/2022 16:08
    SecondaryPool=all
    UserName={os.getlogin()}
    MachineName=OA-MIS-18888
    """

    plugin_info_txt = f"""
    Arguments= -t -x -X {excuteNodes} -- {filePath} <STARTFRAME>,<ENDFRAME>,1
    Executable=I:/script/bin/td/bin/vd2_nuke13.0v2.bat
    Shell=default
    ShellExecute=False
    SingleFramesOnly=False
    StartupDirectory=
    """

    return str(job_info_txt.strip()), str(plugin_info_txt)

# f = open('nuke.json')
# data = json.load(f)
# f.close()

# # jobFile = "J:/vd2/work/prod/cmp/s019/180/vd2_s019_180_cmp_v007.nk"
# # frames = "6144-6300"
# # excuteNodes = "REN_EXR"
# # cores = "16"
# jobFile = data["jobFile"]
# frames = data["frames"]
# excuteNodes = data["frames"]
# cores = data["cores"]
# job_info_txt, plugin_info_txt = GetInfoTxt(jobFile, frames, excuteNodes, cores)

# print(job_info_txt, plugin_info_txt)
# submit_to_deadline(job_info_txt, plugin_info_txt)