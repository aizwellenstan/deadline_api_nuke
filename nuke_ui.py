def _submit_deadline():
    sys.path.append(r'I:\script\bin\td\deadline\submit\python_api')
    
    import submit
    from submit import GetInfoTxtNuke, submit_to_deadline

    pool = _get_pool_str()

    p = nuke.Panel('Submit to Deadline')
    # p.addClipnameSearch('clip path', '/tmp')
    # p.addFilenameSearch('file path', '/tmp')
    # p.addTextFontPulldown('font browser', '/myFonts/')
    # p.addRGBColorChip('some pretty color', '')
    # p.addExpressionInput('enter an expression', '4*25')
    # p.addBooleanCheckBox('yes or no?', True)
    p.addEnumerationPulldown('pool', pool)
    # p.addScriptCommand('tcl or python code', '')
    p.addSingleLineInput('FrameRange', si['tStart'].value()+'-'+si['tEnd'].value())
    # p.addMultilineTextInput('multiple lines of user input text', 'lineA\nlineB')
    # p.addNotepad('write something', 'some very long text could go in here. For now this is just some random default value')
    # p.addPasswordInput('password', 'donttellanyone')
    # p.addButton('push here')
    # p.addButton('or here')
    # p.addButton('or even here')
    p.addSingleLineInput('ChunkSize', "1")
    p.addSingleLineInput('ExcuteNodes', "REN_EXR")
    p.addSingleLineInput('priority', "50")
    p.addSingleLineInput('machineLimit', "40")
    ret = p.show()
    
    if not ret: return

    # iKeyFrame = si['tKeyFrames'].value()
    # frames = iKeyFrame.replace(",", "-")
    # root_name = nuke.Root().name()
    # excuteNodes = "REN_EXR"

    frames = p.value('FrameRange')
    root_name = nuke.Root().name()
    chunkSize = p.value('ChunkSize')
    excuteNodes = p.value('ExcuteNodes')
    pool = p.value('pool')
    priority = p.value('priority')
    machineLimit = p.value('machineLimit')

    job_info_txt, plugin_info_txt = GetInfoTxtNuke(root_name, frames, chunkSize, excuteNodes, pool, priority, machineLimit)
    nuke.message(job_info_txt+""+plugin_info_txt)
    submit_to_deadline(job_info_txt, plugin_info_txt)