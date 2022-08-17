#!/usr/bin/python
# BS"D
# Bentzion Fishman
# 7/31/2022


import PySimpleGUI as sg
import audioFileMetadataController as afc
import audioFileMetadataInjector as afmi
import audioFileHandler as fileHandler

sg.theme('SandyBeach')  # Keep things interesting for your users

albums = ['Album', 'Bava Metziah', 'Parshas Hashavuah', 'Moadim', 'Hilchos Tefilla', 'Shiur Klali', 'Mishna Yomis']

artists = ['Artists', 'Moshe Meiselman', 'Avrahami', 'Fishman', 'Klein', 'Shurkin']

layout = [[sg.Text('Year', size=(3, 0)), sg.InputText(key='year')],
          [sg.Combo(albums, default_value=albums[0], key='album')],
          # [sg.Input(key='-IN-')],
          [sg.Combo(['Rabbi ' + i for i in artists], default_value=artists[0], key='artist')],
          [sg.Checkbox('Is Series', default=False, key='is_series')],
          [sg.Text('Title type', size=(20, 1), font='Lucida', justification='left')],
          [sg.Radio('From file name', 'rd_title', key='from_file_name'),
           sg.Radio('Create file name', 'rd_title', key='from_input_title')],
          [sg.Text("Choose a file: "), sg.FileBrowse(key='full_file_path')],
          [sg.Text('Title', size=(3, 0)), sg.InputText(key='input_title')],
          [sg.Button('Generate'), sg.Button('Exit')]],

window = sg.Window('Tomo File Preprocessor', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Generate':
        values['comment'] = 'Yeshivas Toras Moshe | Ner Michoel Alumni Association'
        values['composer'] = 'NerMichoel.org'
        values['album_art_file_path'] = ''
        values['heb_year'] = '5782'  # we need to grab this from some api it really cannot be hard coded
        '''
        Here's where we tie it all together!
        1. Receive the input data and process it acccordingly to create a dictionary of the metadata
        2. Copy original file and loaded with the metadata from step 1
        3. Compress copy if more than 45 kbps
        4. Prepend original file with '_' if it doesn't already have it
        '''


        m = afc.AudioFileMetaDataController(values)
        file_handler = fileHandler.AudioFileHandler(values['full_file_path'])
        meta_data = {}
        step = 0

        def fail_message(function_name):
            msg = f'failed in: {function_name}'

        try:
            step += 1
            m.updateFileAndTitle()
            meta_data = m.getMetadataDic()
            print(meta_data)
        except Exception as e:
            print(f'step: {step}, error {e}')

        try:
            print('here step 2')
            step += 1

            new_title = 'test-1-' + meta_data['title_tag'] + '.mp3'
            print('here')
            print(f'new title: {new_title}')

            file_handler.copy_file_with_new_title(new_title)

        except Exception as e:
            print(f'step {step}, error: {e}')



    '''
     if event == 'Show':
     # Update the "output" text element to be the value of "input" element
		window['-OUTPUT-'].update(values['-IN-'])


    what needs to happen now:
    1. set the metadata: name, title, album, artists, year,
    2. compress file
    '''

window.close()
