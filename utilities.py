def spm_tissues(in_list):
    '''
    from a SPM NewSegment Tissues list, return GM, WM and CSf

    Example Node:
    spm_tissues_split = Node(
    Function(['in_list'], ['gm', 'wm', 'csf'], spm_tissues), name='spm_tissues_split')

    '''
    return in_list[0][0], in_list[1][0], in_list[2][0]
