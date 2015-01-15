# coding=utf-8
"""


"""
import os.path
import shutil

import pymodelio.core.misc
import pymodelio.core.env



def _copyToLocalWebSpace(projectName, fragment=None, localWebSpace=None ):
    """
    Copy the information from a project to a local space for later web
    publication
    :param projectName: Name of the modelio project to be copied. (referred
    as $PROJECT in the documentation below)
    :type projectName: str
    :param localWebSpaceDirectory: Target directory used for publication.
    (referred as $LIBRARY in the documentation below)
    :type localWebSpaceDirectory: str
    :param fragment: The name of the fragment to be copied. If not specified
    then the name of the fragment will be the name of the project as this is
    the default for all modelio projects. (referred as $MODEL in the
    documentation below).
    :type fragment: str

    The following text comes directly from Modelio documentation and is
    available at http://forge.modelio.org/projects/modelio3-usermanual-english-310/wiki/Distant_libraries_lifecycle

        Lets name the directory of the library project $PROJECT and the work
        model in which the library model resides $MODEL.

        1 Prepare an empty directory ($LIBRARY in the followings) where the
        files to upload to the server will be prepared.

        2 Copy the content of the $PROJECT/data/fragments/$MODEL/admin
        directory into the $LIBRARY/$MODEL/admin directory.

        3 Copy the content of the $PROJECT/data/fragments/$MODEL/blobs
        directory into the $LIBRARY/$MODEL/blobs directory.

        4.Copy the content of the $PROJECT/data/fragments/$MODEL/model into
        the $LIBRARY/$MODEL/model directory.

        5.Copy the content of the $PROJECT/.runtime/fragments/$MODEL/.index
        into the $LIBRARY/$MODEL/.index directory.

        6.Upload the entire contents of $LIBRARY to the HTTP server hosting
        the library.
    """
    workspace = pymodelio.core.env.PyModelioEnv.MODELIO_WORKSPACE
    project_dir = os.path.join(workspace, projectName)
    if localWebSpace is None:
        localWebSpace = os.path.join(project_dir, 'modweb')  # FIXME: name
    if fragment is None:
        fragment = projectName


    # Check the name of the project  ($PROJECT)
    if not os.path.isdir(project_dir):
        msg = 'Directory "%s" does not exist. Check the project name: "%s"'
        raise ValueError(msg % (project_dir, projectName))

    # Check the name of the fragment
    data_fragment_dir = os.path.join(project_dir,'data','fragments',fragment)
    if not os.path.isdir(data_fragment_dir):
        msg = 'Directory "%s" does not exist. Check the fragment name: "%s"'
        raise ValueError(msg % (data_fragment_dir, fragment))

    #--- Step 1 --- Prepare the target directory
    try:
        pymodelio.core.misc.ensureDirectory(localWebSpace)
    except:
        raise RuntimeError('Cannot create directory "%s"'
                           % localWebSpace)

    #--- Steps 2, 3, 4 --- Copy admin, blobs, model directories from data
    for dir in ['admin', 'blobs', 'model']:
        source = os.path.join(data_fragment_dir, dir)
        target = os.path.join(localWebSpace ,fragment,dir)
        if os.path.isdir(target):
            shutil.rmtree(target)
        shutil.copytree(source, target)

    #--- Step 6 --- Copy .index from .runtime
    dir = '.index'
    source = os.path.join(project_dir,'.runtime','fragments', fragment, dir)
    target = os.path.join(localWebSpace, fragment, dir)
    if os.path.isdir(target):
        shutil.rmtree(target)
    shutil.copytree(source, target)
