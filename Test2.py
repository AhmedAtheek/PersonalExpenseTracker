import csv
from tkinter import Tk, messagebox
from tkinter.filedialog import asksaveasfilename

# Example function to save data to a CSV file
def save_csv(data):
    # Open the file save dialog
    file_path = asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Save as CSV"
    )

    if file_path:  # Check if a file was selected
        try:
            # Write data to the selected file
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Assuming `data` is a list of lists (rows of the CSV)
                writer.writerows(data)

            messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")
    else:
        messagebox.showinfo("Cancelled", "Save operation was cancelled.")

# Example usage within a Tkinter app
if __name__ == "__main__":
    # Sample data for the CSV
    sample_data = [
        ["Name", "Age", "City"],
        ["Alice", 30, "New York"],
        ["Bob", 25, "Los Angeles"],
        ["Charlie", 35, "Chicago"]
    ]

    # Initialize Tkinter root window
    root = Tk()
    root.withdraw()  # Hide the main window

    # Call the save function with sample data
    save_csv(sample_data)
