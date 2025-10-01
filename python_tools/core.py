import os

def rename_basename(fileDir, newKey):
    '''takes the first part of the file and renames'''

    folders = [file for file in os.listdir(fileDir)]

    for folder in folders:
        workingDir = os.path.join(fileDir, folder)
        fileList = [file for file in os.listdir(workingDir)]
        for file in fileList:
            nameData = file.split('_')[1:]
            newFile = '_'.join([newKey, *nameData])
            os.rename(os.path.join(workingDir, file), os.path.join(workingDir, newFile))
        
        print(f'{len(fileList)} files renamed in {workingDir}.')
        

def pad_files(fileDir, padLength: 3, padChar: str):
    '''pad files in dir to padLength with padChar'''

    folders = [file for file in os.listdir(fileDir) if os.path.isdir(os.path.join(fileDir, file))]


    for folder in folders:
        try:
            workingDir = os.path.join(fileDir, folder)
            # breakpoint()
            fileList = [file for file in os.listdir(workingDir) if file.lower().endswith('.txt')]  
            # breakpoint() 
            for file in fileList:
                index = file.split('_')[1]
                newIndex = index.rjust(padLength, padChar)
                newFile = file.replace(index, newIndex)
                # breakpoint()
                os.rename(os.path.join(workingDir, file), os.path.join(workingDir, newFile))
        except Exception as e:
            print(e)
            print("broke at folder level")
        
        print(f'{len(fileList)} files renamed in {workingDir}.')

    files = [file for file in os.listdir(fileDir) if file.lower().endswith('.txt')]
    if len(files) > 0:
        for file in files:
            index = file.split('_')[1]
            newIndex = index.rjust(padLength, padChar)
            newFile = file.replace(index, newIndex)
            os.rename(os.path.join(fileDir, file), os.path.join(fileDir, newFile))

        print("found files in root directory. Renamed those too.")


def rename_files(fileDir, oldKey: str, newKey: str, extension='.txt'):
    '''rename files in dir that contain oldKey. Replaces oldKey with newKey in the filename.'''

    files_in_dir = [file for file in os.listdir(fileDir) if file.lower().endswith(extension)]
    if len(files_in_dir) > 0:

        for file in files_in_dir:
            newFile = file.replace(oldKey, newKey)
            os.rename(os.path.join(fileDir, file), os.path.join(fileDir, newFile))
        
        print(f'{len(files_in_dir)} files renamed in {fileDir}.')
    
    else:
        folders = [file for file in os.listdir(fileDir)]
        if oldKey is not None:
            oldKeyList = [oldKey]*len(folders)
        else:
            oldKeyList = [x for x in folders]
        if newKey is not None:
            newKeyList = [newKey]*len(folders)
        else:
            newKeyList = [str(x+1) for x in range(len(folders))]

        for idx, folder in enumerate(folders):
            workingDir = os.path.join(fileDir, folder)
            fileList = [file for file in os.listdir(workingDir)]
            for file in fileList:
                newFile = file.replace(oldKeyList[idx], newKeyList[idx])
                os.rename(os.path.join(workingDir, file), os.path.join(workingDir, newFile))
            
            print(f'{len(fileList)} files renamed in {workingDir}.')
        
        print(f'{len(folders)} folders renamed in {fileDir}.')
        # breakpoint()

def move_files_ABC(filepath):
    Afiles = [file for file in os.listdir(filepath) if '_A' in file]
    Bfiles = [file for file in os.listdir(filepath) if '_B' in file]
    Cfiles = [file for file in os.listdir(filepath) if '_C' in file]

    if not os.path.exists(os.path.join(filepath, 'A')):
        os.makedirs(os.path.join(filepath, 'A'))
    if not os.path.exists(os.path.join(filepath, 'B')):
        os.makedirs(os.path.join(filepath, 'B'))
    if not os.path.exists(os.path.join(filepath, 'C')):
        os.makedirs(os.path.join(filepath, 'C'))

    for file in Afiles:
        os.rename(os.path.join(filepath, file), os.path.join(filepath, 'A', file))
    
    for file in Bfiles:
        os.rename(os.path.join(filepath, file), os.path.join(filepath, 'B', file))
    
    for file in Cfiles:
        os.rename(os.path.join(filepath, file), os.path.join(filepath, 'C', file))

def add_header(data, header=None):
    '''add a header to the data'''
    if header is not None:
        data.insert(0, header)
    return data

def load_and_edit_files(filepath, header=None):
    '''load the files, slice the data and remove the first column'''
    exportDir = os.path.join(filepath, 'edited')
    if not os.path.exists(exportDir):
        os.makedirs(exportDir)
    folders = [file for file in os.listdir(filepath)]

    for folder in folders:
        if not os.path.exists(os.path.join(exportDir, folder)):
            os.makedirs(os.path.join(exportDir, folder))

        workingDir = os.path.join(filepath, folder)
        fileList = [file for file in os.listdir(workingDir) if file.lower().endswith('.txt')]   

        for file in fileList:
            with open(os.path.join(workingDir, file), 'r') as f:
                data = f.readlines()
            
            newData = []
            newData = [x.strip('\n').split(',') for x in data if x != '\n']

            newData = [x[1:] for x in newData]

            if header is not None:
                newData = add_header(newData, header)

            with open(os.path.join(exportDir, folder, file), 'w') as f:
                for line in newData:
                    f.write(','.join(line) + '\n')
            
            print(f'{file} edited in {exportDir}.')

def config_json(filepath):
    '''Creates a json file storing the details of the data structure'''
    import json
    pass

def preprocess_maria_files(filepath):
    move_files_ABC(filepath)
    rename_basename(filepath, 'LnNP')
    pad_files(filepath, 3, '0')
    load_and_edit_files(filepath, header=['data_type', 'maria'])

