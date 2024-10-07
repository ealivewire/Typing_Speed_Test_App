# PROFESSIONAL PROJECT: Typing Speed Test

# Methods of calculating key metrics:
# Characters per minute (CPM): Total the # of characters for each word successfully typed during the test.
# Words per minute (WPM): Divide the CPM by 5 (de facto international standard)

# Import necessary library(ies):
from datetime import datetime
from random import choices
from time import sleep
from tkinter import *
from tkinter import messagebox
import traceback

# Import the common-word list to be used for this application (contained in 'data.py'):
from data import common_words

# Define constant to store number of words to select at random (from the 'common_words" list) for the current exercise:
NUMBER_OF_WORDS_TO_SELECT = 900

# Define constants for application default font size as well as window's height and width:
FONT_NAME = "Arial"
WINDOW_HEIGHT = 650
WINDOW_WIDTH = 425

# Define constant for setting the length of each test (in seconds):
LENGTH_OF_TEST = 60.0

# Define variable for the GUI (application) window (so that it can be used globally), and make it a TKinter instance:
window = Tk()

# Define variable for designating application for termination
# (part of mechanism to break typing-test 'while' loop without
# generating additional errors):
application_exited = False

# Define list variables for storing words (chosen at random) to display in the application window as well as their
# ending indices relative to the 'words_to_type' widget:
words_to_type = []
words_to_type_indices_end = []

# Define variable for widgets that must be referenced across functions:
txt_high_score = Text()
txt_stats = Text()
txt_words_to_type = Text()
txt_word_typed = Text()
button_test = Button()

# Define variable for image to be displayed at top of application window:
img = None

# Define variables for tracking current-test statistics:
current_test_cpm = 0
current_test_wpm = 0
current_test_time_remaining = LENGTH_OF_TEST

# Define variable to track if a test is in progress:
test_in_progress = False


# DEFINE FUNCTIONS TO BE USED FOR THIS APPLICATION (LISTED IN ALPHABETICAL ORDER BY FUNCTION NAME):
def choose_words():
    """Function to select at random (from the 'common_words" list) words for the current test"""
    try:
        # Choose words at random to use for the current test:
        return choices(common_words, k=NUMBER_OF_WORDS_TO_SELECT)

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (choose_words): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("choose_words", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


def end_test():
    """Function which ends the current test"""
    try:
        global txt_word_typed, current_test_cpm, current_test_wpm, current_test_time_remaining, test_in_progress

        # Display final metrics to user and check if a new high score has been achieved.
        # If an error occurs, exit this application:
        if not show_final_metrics():
            test_in_progress = False
            exit()

        # Reset variable to indicate that test is no longer in progress:
        test_in_progress = False

        # Change state of button to indicate that test is in progress:
        button_test.config(text="Start Test")

        # Get a new set of words to type in preparation for a new test:
        get_words_to_type()

        # Reset test to beginning-of-test state, preparing for subsequent word entry by the user.
        # If an error occurs, exit this application:
        if not reset_test_to_beginning():
            exit()

        # Update the application window to reflect the updates executed above:
        window.update()

    except SystemExit:  # Exiting application.
        exit()

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (end_test): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("end_test", traceback.format_exc())

        # If window object exists, destroy it:
        try:
            window.destroy()
        except:
            pass

        # Exit this application:
        exit()


def get_high_score():
    """Function which retrieves the high score to-date (archived in file 'high_score.txt')"""
    try:
        # Open the high-score archive file, retrieve the current high score, and close the file:
        # (NOTE: If the high-score archive file does not exist, high-score will be set to 0).
        try:
            with open("high_score.txt", mode="r") as file:
                high_score_cpm = int(file.read())
                file.close()
        except FileNotFoundError:  # Archive file not found.
            high_score_cpm = 0

        # Return the retrieved high score to the calling function:
        return high_score_cpm

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (get_high_score): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("get_high_score", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


def get_words_to_type():
    """Function to select words at random and display them in the application window for the user to type during the test"""
    global words_to_type, words_to_type_indices_end

    try:
        # Choose words (at random) for user to type. If an error occurs, return failed-execution indication to the
        # calling function:
        words_to_type = choose_words()
        if not words_to_type:
            return False

        # Comprise one string which contains the selected words:
        words_to_type_string = ""
        for word in words_to_type:
            words_to_type_string += word + " "

        # Display chosen words in the application window (at the designated textbox):
        txt_words_to_type.config(state="normal")
        txt_words_to_type.delete(1.0, 'end')
        txt_words_to_type.tag_configure("center", justify="center")
        txt_words_to_type.insert(1.0, chars=words_to_type_string)
        txt_words_to_type.tag_add("left", "1.0", "end")
        txt_words_to_type.config(wrap=WORD, state="disabled")

        # Capture indices to use when highlighting each word in the 'words_to_type' widget.
        # If an error occurs, return failed-execution indication to the calling function:
        if not get_words_to_type_update_indices():
            return False

        # Return successful-execution indication to the calling function:
        return True

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (get_words_to_type): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("get_words_to_type", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


def get_words_to_type_update_indices():
    """Function which captures indices to use when highlighting each word in the 'words_to_type' widget"""
    global words_to_type, words_to_type_indices_end

    try:
        # Capture ending indices to use when highlighting each word in the 'words_to_type' widget:
        words_to_type_indices_end = []
        i = 0
        for word in words_to_type:
            words_to_type_indices_end.append("1."+str(int(i + len(word)+1)))
            i += len(word)

        # Return successful-execution indication to the calling function:
        return True

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (get_words_to_type_update_indices): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("get_words_to_type_update_indices", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


def handle_window_on_closing():
    """Function which confirms with user if s/he wishes to exit this application"""
    global application_exited

    # Confirm with user if s/he wishes to exit this application:
    if messagebox.askokcancel("Exit?", "Do you want to exit this application?"):
        # Designate application for termination:
        application_exited = True

        # Destroy the application window:
        window.destroy()

        # Exit this application:
        exit()


def highlight_current_word(start_index, end_index):
    """Function to highlight the current word in the 'txt_words_to_type' widget"""
    try:
        # Highlight current word:
        txt_words_to_type.tag_add("start", start_index, end_index)
        txt_words_to_type.tag_config("start", background="yellow", foreground="blue")

        # Update the application window to reflect the updates executed above:
        window.update()

        # Return successful-execution indication to the calling function:
        return True

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (highlight_current_word): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("highlight_current_word", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


def reset_test_to_beginning():
    """Function which clears the entry widget of its contents and performs supporting functionality"""
    global current_test_cpm, current_test_wpm, current_test_time_remaining

    try:
        # Clear the entry widget of its contents, preparing for subsequent word entry by the user:
        txt_word_typed.config(state="normal")
        txt_word_typed.delete(0, "end")
        txt_word_typed.insert(0, "")

        # If test is not in progress (e.g., in "beginning-of-test" state), perform the following:
        if not test_in_progress:
            # Reset CPM, WPM, and remaining time metrics in preparation for a new test:
            current_test_cpm = 0
            current_test_wpm = 0
            current_test_time_remaining = LENGTH_OF_TEST

            # Update the application with the beginning-of-test statistics (i.e., CPM, WPM, remaining time).
            # If an error occurs, return failed-execution indication to the calling function:
            if not update_stats():
                return False

            # Reset contents for (and disable) the entry widget:
            txt_word_typed.delete(0, "end")
            txt_word_typed.insert(0, "Press 'Start Test' button below to begin test.")
            txt_word_typed.config(state="disabled")

            # Change state of button to indicate that test is NOT in progress:
            button_test.config(text="Start Test", command=run_test)

        # Set focus on the entry widget:
        txt_word_typed.focus()

        # Update the application window to reflect the updates executed above:
        window.update()

        # Return successful-execution indication to the calling function:
        return True

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (reset_test_to_beginning): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("reset_test_to_beginning", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


def run_app():
    """Main function used to run this application"""
    try:
        # Creates and configure all visible aspects of the application window.  If an error occurs,
        # exit this application:
        if not window_config():
            exit()

        # Select words at random and display them in the application window for the user to type during the test.
        # If an error occurs, exit this application:
        if not get_words_to_type():
            exit()

        # From this point, test will start and end based on user's use of the start/end button, with subsequent
        # functionality defined from there.

    except SystemExit:  # Exiting application.
        exit()

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (run_app): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("run_app", traceback.format_exc())

        # If window object exists, destroy it:
        try:
            window.destroy()
        except:
            pass

        # Exit this application:
        exit()


def run_test():
    """Function which runs the typing test"""
    global current_test_cpm, current_test_wpm, current_test_time_remaining, test_in_progress, application_exited

    try:
        # Reset CPM, WPM, and remaining time metrics in preparation for a new test:
        current_test_cpm = 0
        current_test_wpm = 0
        current_test_time_remaining = LENGTH_OF_TEST

        # Update the application with the beginning-of-test statistics (i.e., CPM, WPM, remaining time).
        # If an error occurs, exit this application:
        if not update_stats():
            exit()

        # Change state of button to indicate that test is in progress:
        button_test.config(text="End Test", command=end_test)

        # Indicate that a new test is now in progress (used in the 'while' loop below):
        test_in_progress = True

        # Reset test to beginning-of-test state, preparing for subsequent word entry by the user.
        # If an error occurs, exit this application:
        if not reset_test_to_beginning():
            exit()

        # Count down the time remaining in the current test. Also, update the current CPM and WPM stats after each successfully typed word:
        i = 0  # Index of the current word:
        while test_in_progress:
            # If no time remains in the current test, end the test:
            if current_test_time_remaining <= 0:
                test_in_progress = False
                end_test()  # If error occurs in ending test, the "end_test" function itself will exit this application.

            else:  # Time remains on the current test.
                # If all of the words to type have NOT been completed, highlight the word to text and respond to user's entry:
                if i < len(words_to_type):
                    # Highlight, in YELLOW, the current word in the 'words_to_type' widget indicate in-progress state.
                    # If an error occurs, exit this application:
                    if not highlight_current_word("1.0", words_to_type_indices_end[0]):
                        test_in_progress = False
                        exit()

                    # If user has fully and correctly typed the current word, remove it from the 'words_to_type' widget,
                    # and associated variables, and update the CPM and WPM stats so far for this test:
                    if txt_word_typed.get() == words_to_type[0]:
                        # Clear out the user entry widget:
                        txt_word_typed.delete(0, END)

                        # Remove the word from the 'words_to_type' widget:
                        txt_words_to_type.config(state='normal')
                        txt_words_to_type.delete("1.0", words_to_type_indices_end[0])
                        txt_words_to_type.config(state='disabled')

                        # Update the CPM and WPM totals for the current test:
                        current_test_cpm += len(words_to_type[i])
                        current_test_wpm = int(round(current_test_cpm / 5, 0))

                        # Remove the word and its ending index from relevant variables:
                        del words_to_type[0]

                        # Update indices.  If an error occurs, exit this application:
                        if not get_words_to_type_update_indices():
                            test_in_progress = False
                            exit()

                else:  # All words have been typed in fully and correctly.
                    test_in_progress = False
                    end_test()  # If error occurs in ending test, the "end_test" function itself will exit this application.

                # Deduct 0.01 seconds from the remaining time for the current test:
                current_test_time_remaining -= 0.01
                sleep(0.01)

                # Update the application with the current test's statistics (i.e., CPM, WPM, remaining time).
                # If an error occurs, exit this application:
                if not update_stats():
                    test_in_progress = False
                    exit()

                # Update the application window to reflect the updates executed above:
                window.update()

    except SystemExit:  # Exiting application.
        exit()

    except:  # An error has occurred.
        # Indicate that typing test is no longer in progress:
        test_in_progress = False

        # Inform user:
        messagebox.showinfo("Error", f"Error (run_test): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("run_test", traceback.format_exc())

        # If window object exists, destroy it:
        try:
            window.destroy()
        except:
            pass

        # Exit this application:
        exit()


def show_final_metrics():
    """Function to show the final metrics (i.e., CPM and WPM) for the current test (including info. on if a new high score has been achieved)"""
    try:
        # Capture the high score previous to the current test.  If an error occurs, return
        # failed-execution indication to the calling function:
        previous_high_score_cpm = get_high_score()
        if not previous_high_score_cpm:
            return False
        previous_high_score_wpm = int(round(previous_high_score_cpm / 5, 0))

        # If a new high score has been achieved, archive it and include as part of the final-metrics message box to user:
        if current_test_cpm > previous_high_score_cpm:  # New high score has been achieved.
            # Archive the new high score.  If an error occurs, return failed-execution indication to the calling function:
            if not update_high_score(current_test_cpm):
                return False

            # Prepare an "addendum" to the final-metrics message box to be shown to the user:
            high_score_added_message = f"\n\nYou have achieved a new high score!:\nPrevious high score:\nCPM: {previous_high_score_cpm}\nWPM: {previous_high_score_wpm}"

        else:  # New high score has NOT been achieved.
            high_score_added_message = ""

        # Display the final-metrics message box to the user:
        messagebox.showinfo(title="Test has ended", message=f"FINAL METRICS:\nCPM: {current_test_cpm}\nWPM: {current_test_wpm}{high_score_added_message}")

        # Return successful-execution indication to the calling function:
        return True

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (show_final_metrics): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("show_final_metrics", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


def update_high_score(new_high_score_cpm):
    """Function which archives a new high score to file 'high_score.txt'"""
    global txt_high_score

    try:
        # Open the high-score archive file, store the new high score, and close the file:
        with open("high_score.txt", mode="w") as file:
            file.write(str(new_high_score_cpm))
            file.close()

        # Update the application window to show the new high score:
        new_high_score_wpm = int(round(new_high_score_cpm / 5, 0))
        txt_high_score.config(state="normal")
        txt_high_score.tag_configure("center", justify='center')
        txt_high_score.replace(1.0, END, "HIGH SCORE: " + str(new_high_score_cpm) + " CPM (" + str(new_high_score_wpm) + " WPM)")
        txt_high_score.tag_add("center", "1.0", "end")
        txt_high_score.config(state="disabled")

        # Return successful-execution indication to the calling function:
        return True

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (update_high_score): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("update_high_score", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


def update_stats():
    """Function which updates the application window with the current test's statistics"""
    global current_test_cpm, current_test_wpm, current_test_time_remaining

    try:
        # Update the application window to show the current test's statistics (i.e., CPM, WPM, remaining time):
        txt_stats.config(state="normal")
        txt_stats.tag_configure("center", justify='center')
        txt_stats.replace(1.0, END, "CPM: " + str(current_test_cpm) + "     WPM: " + str(current_test_wpm) + "     Remaining Time: " + str(abs(round(current_test_time_remaining,1))))
        txt_stats.tag_add("center", "1.0", "end")
        txt_stats.config(state="disabled")

        # Return successful-execution indication to the calling function:
        return True

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (update_stats): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("update_stats", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


def update_system_log(activity, log):
    """Function to update the system log with errors encountered"""
    try:
        # Capture current date/time:
        current_date_time = datetime.now()
        current_date_time_file = current_date_time.strftime("%Y-%m-%d")

        # Update log file.  If log file does not exist, create it:
        with open("log_typing_speed_test_app_" + current_date_time_file + ".txt", "a") as f:
            f.write(datetime.now().strftime("%Y-%m-%d @ %I:%M %p") + ":\n")
            f.write(activity + ": " + log + "\n")

        # Close the log file:
        f.close()

    except:  # An error has occurred.
        messagebox.showinfo("Error", f"Error: System log could not be updated.\n{traceback.format_exc()}")


def window_center_screen():
    """Function which centers the application window on the computer screen"""
    try:
        # Capture the desired width and height for the window:
        w = WINDOW_WIDTH # width of tkinter window
        h = WINDOW_HEIGHT  # height of tkinter window

        # Capture the computer screen's width and height:
        screen_width = window.winfo_screenwidth()  # Width of the screen
        screen_height = window.winfo_screenheight()  # Height of the screen

        # Calculate starting X and Y coordinates for the application window:
        x = (screen_width / 2) - (w / 2)
        y = (screen_height / 2) - (h / 2)

        # Center the application window based on the aforementioned constructs:
        window.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Return successful-execution indication to the calling function:
        return True

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (window_center_screen): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("window_center_screen", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


def window_config():
    """Function which creates and configures all visible aspects of the application window"""
    try:
        # Create and configure application window.  If an error occurs, return
        # failed-execution indication to the calling function:
        if not window_create_and_config():
            return False

        # Create and configure user interface.  If an error occurs, return failed-execution
        # indication to the calling function:
        if not window_create_and_config_user_interface():
            return False

        # Return successful-execution indication to the calling function:
        return True

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (window_config): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("window_config", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


def window_create_and_config():
    """Function to create and configure the GUI (application) window"""
    global img

    try:
        # Create and configure the application window:
        window.title("My Typing Speed Tester")
        window.minsize(width=520, height=400)
        window.config(padx=45, pady=0,bg='white')
        window.resizable(0, 0)  # Prevents window from being resized.
        window.attributes("-toolwindow", 1)  # Removes the minimize and maximize buttons from the application window.

        # Center the application window on the computer screen.  If an error occurs, return failed-execution
        # indication to the calling function:
        if not window_center_screen():
            return False

        # Prepare the application to handle the event of user attempting to close the application window:
        window.protocol("WM_DELETE_WINDOW", handle_window_on_closing)

        # Return successful-execution indication to the calling function:
        return True

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (window_create_and_config): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("window_create_and_config", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


def window_create_and_config_user_interface():
    """Function which creates and configures items comprising the user interface, including the canvas (which overlays on top of the app. window), labels, textboxes, and button"""
    global txt_high_score, txt_stats, txt_words_to_type, txt_word_typed, button_test, img

    try:
        # Create and configure canvas which overlays on top of window:
        canvas = Canvas(window)
        img = PhotoImage(file="keyboard.png")
        canvas.config(height=img.height(), width=WINDOW_WIDTH, bg='white', highlightthickness=0)
        canvas.create_image(210,54, image=img)
        canvas.grid(column=0, row=3, columnspan=2, padx=0, pady=0)
        canvas.create_line(0, 0, 500, 0)
        canvas.update()

        # Get high score for display (archived in file 'high_score.txt'),  If an error occurs, return failed-execution
        # indication to the calling function:
        high_score_cpm = get_high_score()
        if not high_score_cpm:
            return False
        high_score_wpm = int(round(high_score_cpm / 5, 0))

        # Create and configure text widget to show the high score:
        txt_high_score = Text(window, width=50, height=0, bg='white', fg='black', padx=0, pady=0, bd=0, borderwidth=0, highlightthickness=0, font=(FONT_NAME,10,"bold"))
        txt_high_score.grid(column=0, row=0, columnspan=2)
        txt_high_score.tag_configure("center", justify='center')
        txt_high_score.insert(1.0, "HIGH SCORE: " + str(high_score_cpm) + " CPM (" + str(high_score_wpm) + " WPM)")
        txt_high_score.tag_add("center", "1.0", "end")
        txt_high_score.config(state="disabled")

        # Create and configure text widget to show stats for current test (CPM, WPM, Remaining Time):
        txt_stats = Text(window, width=60, height=0, bg='white', fg='black', padx=0, pady=10, bd=0, borderwidth=0, highlightthickness=0, font=(FONT_NAME,10,"bold"))
        txt_stats.grid(column=0, row=1, columnspan=2)
        txt_stats.tag_configure("center", justify='center')
        txt_stats.insert(1.0, "CPM: " + "0" + "     WPM: " + "0" + "     Remaining Time: " + str(LENGTH_OF_TEST))
        txt_stats.tag_add("center", "1.0", "end")
        txt_stats.config(state="disabled")

        # Create and configure the header text (label) above the words user must type:
        label_words_to_type_header = Label(text="Words to Type (Max = " + str(NUMBER_OF_WORDS_TO_SELECT) + ")", height=2, bg='white', fg='black', padx=0, pady=0, font=(FONT_NAME,16, "bold"))
        label_words_to_type_header.grid(column=0, row=4, columnspan=2)

        # Create and configure the text widget for displaying the words user must type:
        txt_words_to_type = Text(window, width=35, height=12, bg='white', fg='blue', padx=0, pady=0, bd=0, borderwidth=0, highlightthickness=0, font=(FONT_NAME,14,"normal"))
        txt_words_to_type.grid(column=0, row=5, columnspan=2)

        # Create and configure the entry widget for displaying the contents of what the user has typed:
        txt_word_typed = Entry(window, width=35, bg='white', fg='red', font=(FONT_NAME,14,"normal"), justify="center")
        txt_word_typed.delete(0, "end")
        txt_word_typed.insert(0, "Press 'Start Test' button below to begin test.")
        txt_word_typed.grid(column=0, row=6, columnspan=2, pady=10)
        txt_word_typed.config(state="disabled")

        # Create and configure the blank "label" which serves as a separator between the 'words to type' text and the button:
        label_space = Label(text="Words to Type:", bg='white', fg='white', padx=0, pady=0, font=(FONT_NAME,16, "bold"))
        label_space.grid(column=0, row=7)

        # Create and configure button used to either start or end the current game:
        button_test = Button(text="Start Test", width=20, height=1, bg='red', fg='white', pady=0, font=(FONT_NAME,16,"bold"), command=run_test)
        button_test.grid(column=0, row=8,columnspan=2)

        # Return successful-execution indication to the calling function:
        return True

    except:  # An error has occurred.
        # Inform user:
        messagebox.showinfo("Error", f"Error (window_create_and_config_user_interface): {traceback.format_exc()}")

        # Update system log with error details:
        update_system_log("window_create_and_config_user_interface", traceback.format_exc())

        # Return failed-execution indication to the calling function:
        return False


# Run this application:
run_app()

# Keep application window open until user closes it:
window.mainloop()

if __name__ == '__main__':
    run_app()



