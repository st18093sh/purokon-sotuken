import PySimpleGUI as sg

layout = [  [sg.Text('録画を開始する際はSTARTボタンを、終了する際はSTOPボタンを押してください。')],
            [sg.Text('STOPボタンを押すと分析が始まります。結果が出るまでお待ちください。')],
            [sg.Text('ENDボタンでウィンドウが閉じます。')],
            [sg.Button('START', size=(10, 1)), sg.Button('STOP', size=(10, 1)), sg.Button('END', size=(10, 1))],
            [sg.Output(size=(200, 40))] ]

window = sg.Window('TSUWA', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'END':
        break

    elif event == 'START':
        break

    elif event == 'STOP':
        break

window.close()
