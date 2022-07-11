import PySimpleGUI as PySG
import validator as vad
import pyperclip

website_list = []

def set_layout():
    # All the stuff inside your window.

    websites_layout = [

        [PySG.Text("WebSite Watcher V0.1", size=(30, 1), font=("Helvetica", 25), pad=(10, 0))],

        [PySG.InputText("Enter a Web Site", key="-WEBSITE_NAME-", size=(57, 10), pad=(10, 0)),
         PySG.Button("Validate", size=(10, 1))],

        [PySG.Listbox(key="-WEBSITE_LISTBOX-", values=[], size=(55, 10), pad=(10, 0)),
         PySG.Column([[PySG.Button("Delete", size=(10, 1))],
                      [PySG.Button("Copy", size=(10, 1))],
                      [PySG.Button("Confirm", size=(10, 1))],
                      ])],

        [PySG.InputText(key='-FILENAME-', disabled=True, size=(57, 1), text_color="grey2", pad=(10, (10, 0))),
         PySG.FileBrowse(size=(10, 1), pad=((5, 0), (5, 0)))],

        [PySG.Button("Upload", size=(10, 1), pad=(10, 10)), PySG.Button("Save", size=(10, 1), pad=(10, 10))],

    ]

    check_websites_layout = [

        [PySG.Text("WebSite Watcher V0.2", size=(30, 1), font=("Helvetica", 25))],
    ]

    tab_group = [
        [PySG.TabGroup(
            [[
                PySG.Tab("Websites", websites_layout),
                PySG.Tab("Monitor", check_websites_layout),
            ]]
        )]
    ]

    return tab_group


def generate_gui(layout):
    # Create the Window
    window = PySG.Window("SiteWatch", layout, margins=(10, 5))

    while True:  # Event Loop
        event, values = window.read()
        print(event, values)

        if event == PySG.WIN_CLOSED or event == "Exit":
            break

        if event == "Browse":
            pass

        if event == "Validate":
            if vad.is_valid_url(values["-WEBSITE_NAME-"]):
                window["-WEBSITE_NAME-"].update(text_color="green2")
                website_list.append(values["-WEBSITE_NAME-"])
                window["-WEBSITE_LISTBOX-"].update(website_list)
            else:
                window["-WEBSITE_NAME-"].update(text_color="red2")

        if event == "Delete":
            website_list.pop(window["-WEBSITE_LISTBOX-"].get_indexes()[0])
            window["-WEBSITE_LISTBOX-"].update(website_list)
        if event == "Copy":
            pyperclip.copy(website_list[window["-WEBSITE_LISTBOX-"].get_indexes()[0]])

    window.close()


################################################################################
# TESTS                                                                        #
################################################################################
def test_func():
    return True


def test():
    if test_func():
        return True
    # print("All Testing Completed Successfully!")


################################################################################
# MAIN                                                                         #
################################################################################
def main():
    if test():
        # STYLE
        PySG.theme("DarkGrey11")
        PySG.set_options(font=("Arial", 12))

        # MAIN
        generate_gui(set_layout())


if __name__ == "__main__":
    main()
