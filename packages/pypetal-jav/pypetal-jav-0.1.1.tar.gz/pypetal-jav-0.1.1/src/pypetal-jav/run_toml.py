import toml
import numpy as np

import os
import glob


def str2none(x):
    if x == 'None':
        return None
    else:
        return x

#########################################################################################
################################# ASSIST FUNCTIONS ######################################
#########################################################################################

def make_toml(output_dir, fnames, 
              run_arr, param_arr,
              line_names=None, filename=None):

    tot_keys = ['drw_rej', 'detrend', 'pyccf', 'pyzdcf', 'pyroa', 'javelin', 'weighting']
    toml_dict = {}


    #Inputs
    toml_dict['inputs'] = {}
    toml_dict['inputs']['output_dir'] = output_dir
    toml_dict['inputs']['filenames'] = fnames

    if line_names is not None:
        toml_dict['inputs']['line_names'] = line_names





    toml_dict['params'] = {}

    #General parameters
    if param_arr[0] != {}:
        toml_dict['params']['general'] = param_arr[0]


    #Module parameters
    for i in range(len(run_arr)):
        if run_arr[i]:
            toml_dict['params'][tot_keys[i]] = param_arr[i+1]

    #Write to file
    if filename is not None:
        toml.dump(toml_dict, open(filename, 'w+'))

    return toml_dict





def get_toml_modules(filename):

    tot_keys = ['drw_rej', 'detrend', 'pyccf', 'pyzdcf', 'pyroa', 'javelin', 'weighting']
    run_arr = []

    toml_dat = toml.load(filename)['params']

    for key in tot_keys:
        if key in toml_dat.keys():
            if 'run' in toml_dat[key]:
                run_val = toml_dat[key]['run']
            else:
                run_val = False
        else:
            run_val = False


        run_arr.append(run_val)

    return run_arr




def get_toml_params(filename, run_arr):
    
    tot_keys = ['drw_rej', 'detrend', 'pyccf', 'pyzdcf', 'pyroa', 'javelin', 'weighting']
    param_arr = []


    toml_dat = toml.load(filename)['params']

    #General parameters
    if 'general' in toml_dat.keys():
        param_arr.append(toml_dat['general'])
    else:
        param_arr.append({})


    #Module parameters
    for i in range(len(run_arr)):

        if run_arr[i]:
            param_arr.append(toml_dat[tot_keys[i]])
        else:
            param_arr.append({})

    return param_arr








def get_toml_inputs(filename):

    toml_dat = toml.load(filename)

    assert 'inputs' in toml_dat.keys(), 'No inputs found in toml file'
    assert 'output_dir' in toml_dat['inputs'].keys(), 'No output directory found in toml file'        
    assert 'filenames' in toml_dat['inputs'].keys(), 'No filenames found in toml file'


    #################################
    #Output directory
    
    output_dir = os.path.abspath(toml_dat['inputs']['output_dir']) + r'/'


    #################################
    #Filenames

    #If input is a list
    if isinstance( toml_dat['inputs']['filenames'], list ):
        for i in range(len(toml_dat['inputs']['filenames'])):
            assert os.path.isfile(toml_dat['inputs']['filenames'][i]), 'File not found: ' + toml_dat['inputs']['filenames'][i]

        filenames = toml_dat['inputs']['filenames']



    #If input is a string
    if isinstance( toml_dat['inputs']['filenames'], str ):
        exists = os.path.exists(toml_dat['inputs']['filenames'])
        isdir = os.path.isdir(toml_dat['inputs']['filenames'])


        #Assume all files in directory are inputs
        if exists and isdir:
            filenames = glob.glob(toml_dat['inputs']['filenames']+'*')

        #Assume input is a glob pattern
        elif exists and (not isdir):
            filenames = glob.glob(toml_dat['inputs']['filenames'])
            assert len(filenames) > 0, 'No files found matching glob pattern: ' + toml_dat['inputs']['filenames']


        for i in range(len(filenames)):
            assert os.path.isfile(filenames[i]), 'File not found: ' + filenames[i]




    #################################
    #Line names

    if str2none(toml_dat['inputs']['line_names']) is None:
        line_names = []
        for i in range(len(filenames)):
            line_names.append('Line {}'.format(i+1))

    else:
        assert isinstance( toml_dat['inputs']['line_names'], list ), 'Line names must be a list'
        line_names = toml_dat['inputs']['line_names']

    return output_dir, filenames, line_names



#########################################################################################
################################ TO RUN SINGLE OBJECTS ##################################
#########################################################################################
    
#Run javelin
def run_from_toml_jav(filename):
    import pypetal_jav.pipeline as pl
    
    output_dir, _, line_names = get_toml_inputs(filename)
    run_arr = get_toml_modules(filename)
    param_arr = get_toml_params(filename, run_arr)

    if 'use_for_javelin' in param_arr[1]:
        use_for_javelin = param_arr[1]['use_for_javelin']
    else:
        use_for_javelin = False
    
    
    if use_for_javelin:
        if 'reject_data' in param_arr[1]:
            reject_data = param_arr[1]['reject_data']
        else:
            reject_data = np.zeros(len(line_names), dtype=bool)
            reject_data[0] = True
            
            
        taus = []
        sigs = []
        jits = []
        for i in range(len(line_names)):
            if reject_data[i]:
                s, t, j = np.loadtxt( output_dir + line_names[i] + '/drw_rej/' + line_names[i] + '_chain.dat', 
                                      unpack=True, delimiter=',', usecols=[0,1,2] )
        
                sigs.append(s)
                taus.append(t)
                jits.append(j)
                
        drw_rej_res = {
            'reject_data': reject_data,
            'taus': taus,
            'sigmas': sigs,
            'jitters': jits
        }
    else:
        drw_rej_res = {}
    
    
    if run_arr[-2]:
        res = pl.run_pipeline(output_dir, line_names,
                              javelin_params=param_arr[6], use_for_javelin=use_for_javelin,
                              drw_rej_res=drw_rej_res,
                              **param_arr[0])
        
        return res

    else:
        return
    
    
#########################################################################################
################################ TO RUN MULTIPLE OBJECTS ################################
#########################################################################################

def run_all2(filenames):
    for f in filenames:
        _ = run_from_toml_jav(f)
        
    return
