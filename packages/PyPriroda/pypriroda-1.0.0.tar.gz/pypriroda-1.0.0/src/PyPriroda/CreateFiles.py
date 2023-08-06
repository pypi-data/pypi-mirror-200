import os

#path = os.path.join(os.path.dirname(__file__), 'ex.txt')
pth = os.path.dirname(__file__) #path to directory where we run code

def create_optim(name_of_out_hess_file = 'name'):
    '''
    Function creates a hessian from the optimization file
    Parameters
    ----------
    name_of_hess_file : string, default= 'name'. The name of the hessian file, 
    where the coordinates and the energies come from
    If 'name', the function takes the name of
    the hessian file from keybord.
    '''

    if name_of_out_hess_file == 'name':

        print('Enter the name of output hessian file')
        print('in format name.out')
        name_of_out_hess_file = input()


    #All the information that we should write in (almost) all optimization files
    head_of_optimization_file = ['$system memory=1024 disk=100 path=. $end', 
                                 '$control ', 
                                 ' task=optimize  ', 
                                 ' theory=DFT four=1', 
                                 ' basis=basis4.bas $end', 
                                 '$grid acc=1e-8 $end', 
                                 '$scf conv=1e-6 proc=BFGS iter=200 $end', 
                                 '$optimize saddle=1 follow=1 tolerance=1e-5 trust=0.01 steps=10 $end', 
                                 '$molecule ', ' charge=0 ', ' mult=2', 
                                 ' cartesian', ' set=L1 ', '$end', 
                                 '$Energy', '$end']
    
    #We need to take the coordinates and the energies out of the hess-file

    
    #pth: the directory where we run code
    with open(os.path.join(pth, name_of_out_hess_file), 'r') as f:
        content = [i.replace('\n', '').replace('eng>', ' ') for i in f.readlines()]
    
    index_of_start_coordinates = 0
    index_of_end_coordinates = 0
    index_of_start_energy = 0
    index_of_end_energy = 0

    for i in range(len(content)):

        if content[i] == ' Atomic Coordinates:':
            index_of_start_coordinates = i
            continue

        if content[i] == ' #':
            index_of_end_coordinates = i
            continue

        if content[i] == ' $Energy': 
            index_of_start_energy = i
            continue

        if content[i] == ' $end':
            index_of_end_energy = i
            break
    

                      #head of file                                              #coordinates                                  #$end $Energy                           #Energy                                         #$end
    write_into_file = head_of_optimization_file[:13] + content[index_of_start_coordinates+1:index_of_end_coordinates] + head_of_optimization_file[13:15] + content[index_of_start_energy+1:index_of_end_energy] + head_of_optimization_file[15:]

    final_text = '\n'.join(write_into_file)

    #Name of the out file  
    # in the format: optim_name.in
    name_of_final_in_file = 'optim_' + name_of_out_hess_file.replace('.out', '.in')

    with open(os.path.join(pth, name_of_final_in_file), 'w') as f:
        f.write(final_text)

    print('Name of our input optimization file')
    print(name_of_final_in_file)
    



def create_hess(name_of_out_optimization_file='name'):
    '''
    Function creates hessian from an optimization file
    Parameters
    ----------
    name_of_out_optimization_file : string, default= 'name'. 
    The name of the optimization file, where the coordinates and the energies come from.
    If 'name', the function takes the name of
    the optimization file from keybord.
    '''

    if name_of_out_optimization_file == 'name':

        print('Enter the name of output optimization file')
        print('in format name.out')

        name_of_out_optimization_file = input()

    #All the information that we should write in (almost) all optimization files
    head_of_hess_file = ['$system memory=1024 disk=6 path=. $end', 
            '$control task=hessian theory=DFT four=1 basis=basis4.in $end', 
            '$scf conv=1e-6 proc=BFGS iter=200 $end', '$grid acc=1e-8 $end', 
            '$end', '$molecule charge=0 mult=2 cartesian set=L1', '$end', 
            '$integral ', 'direct=1 ', '$end']
    

    #We need to take the atomic coordinates out of the optimization file
    #pth: the directory where we run code
    with open(os.path.join(pth, name_of_out_optimization_file), 'r') as f:
        content = [i.replace('\n', '').replace('eng>', ' ') for i in f.readlines()]
    
    index_of_end_of_coordinates = 0
    index_of_beginning_of_coordinates = 0

    #Read the optim-file from the end, 
    # because we need the last step of the optimization
    for i in range(len(content)-1, -1, -1):
        if content[i] == ' #': #the end of the coordinates 
            index_of_end_of_coordinates = i
            continue
        if content[i] == ' Atomic Coordinates:':
            index_of_beginning_of_coordinates = i
            break
    
    write_into_file = head_of_hess_file[:6] + content[index_of_beginning_of_coordinates+1:index_of_end_of_coordinates] + head_of_hess_file[6:]
    final_text = '\n'.join(write_into_file)

    name_of_hess_in_file = 'HESS_' + name_of_out_optimization_file.replace('.out', '.in')

    with open(os.path.join(pth, name_of_hess_in_file), 'w') as f:
        f.write(final_text)

    print('Name of our input hessian file')
    print(name_of_hess_in_file)

