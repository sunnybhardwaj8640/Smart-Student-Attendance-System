import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import os
from tkinter import font as tkfont

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Attendance System")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Configure style
        self.configure_styles()
        
        # Create data directory if it doesn't exist
        if not os.path.exists('attendance_data'):
            os.makedirs('attendance_data')
            
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.csv_file = f"attendance_data/attendance_{self.current_date}.csv"
        
        self.setup_ui()
        
    def configure_styles(self):
        """Configure custom styles for the application"""
        self.style = ttk.Style()
        
        # Configure theme
        self.style.theme_use('clam')
        
        # Configure colors
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10), padding=5)
        self.style.configure('TEntry', font=('Helvetica', 10), padding=5)
        self.style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'), foreground='#2c3e50')
        self.style.configure('Treeview', font=('Helvetica', 10), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))
        self.style.map('TButton', 
                      foreground=[('pressed', 'white'), ('active', 'white')],
                      background=[('pressed', '#3498db'), ('active', '#2980b9')])
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Main container frame
        self.main_frame = ttk.Frame(self.root, padding="15")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header section
        self.setup_header()
        
        # Input section
        self.setup_input_section()
        
        # Button section
        self.setup_button_section()
        
        # Records section
        self.setup_records_section()
        
        # Load existing records
        self.load_records()
    
    def setup_header(self):
        """Setup the header section"""
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Title label
        self.title_label = ttk.Label(
            self.header_frame, 
            text="SMART ATTENDANCE SYSTEM", 
            style='Header.TLabel'
        )
        self.title_label.pack(side=tk.LEFT)
        
        # Date label
        self.date_label = ttk.Label(
            self.header_frame, 
            text=f"Date: {self.current_date}",
            font=('Helvetica', 10, 'italic')
        )
        self.date_label.pack(side=tk.RIGHT)
    
    def setup_input_section(self):
        """Setup the student information input section"""
        self.input_frame = ttk.LabelFrame(
            self.main_frame, 
            text=" Student Information ",
            padding=(15, 10)
        )
        self.input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Configure grid
        self.input_frame.columnconfigure(1, weight=1)
        
        # Student ID
        ttk.Label(self.input_frame, text="Student ID:").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.id_entry = ttk.Entry(self.input_frame)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Student Name
        ttk.Label(self.input_frame, text="Student Name:").grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = ttk.Entry(self.input_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Department
        ttk.Label(self.input_frame, text="Department:").grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.dept_entry = ttk.Entry(self.input_frame)
        self.dept_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Status
        ttk.Label(self.input_frame, text="Status:").grid(
            row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.status_var = tk.StringVar(value="Present")
        self.status_combobox = ttk.Combobox(
            self.input_frame, 
            textvariable=self.status_var,
            values=["Present", "Absent", "Late"],
            state="readonly"
        )
        self.status_combobox.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Set focus to ID entry
        self.id_entry.focus_set()
    
    def setup_button_section(self):
        """Setup the button section"""
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Configure grid for buttons
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.columnconfigure(3, weight=1)
        
        # Submit button
        self.submit_button = ttk.Button(
            self.button_frame, 
            text="Submit Attendance", 
            command=self.submit_attendance,
            style='TButton'
        )
        self.submit_button.grid(row=0, column=0, padx=5, sticky=tk.EW)
        
        # View button
        self.view_button = ttk.Button(
            self.button_frame, 
            text="View Records", 
            command=self.view_records
        )
        self.view_button.grid(row=0, column=1, padx=5, sticky=tk.EW)
        
        # Export button
        self.export_button = ttk.Button(
            self.button_frame, 
            text="Export to CSV", 
            command=self.export_to_csv
        )
        self.export_button.grid(row=0, column=2, padx=5, sticky=tk.EW)
        
        # Clear button
        self.clear_button = ttk.Button(
            self.button_frame, 
            text="Clear Fields", 
            command=self.clear_fields
        )
        self.clear_button.grid(row=0, column=3, padx=5, sticky=tk.EW)
    
    def setup_records_section(self):
        """Setup the attendance records display section"""
        self.records_frame = ttk.LabelFrame(
            self.main_frame, 
            text=" Attendance Records ",
            padding=(10, 5)
        )
        self.records_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure treeview columns
        columns = ("id", "name", "dept", "status", "time")
        
        # Create treeview with scrollbar
        self.records_tree = ttk.Treeview(
            self.records_frame, 
            columns=columns, 
            show="headings",
            selectmode="extended"
        )
        
        # Define headings
        self.records_tree.heading("id", text="Student ID", anchor=tk.CENTER)
        self.records_tree.heading("name", text="Name", anchor=tk.W)
        self.records_tree.heading("dept", text="Department", anchor=tk.W)
        self.records_tree.heading("status", text="Status", anchor=tk.CENTER)
        self.records_tree.heading("time", text="Time", anchor=tk.CENTER)
        
        # Define column widths
        self.records_tree.column("id", width=120, anchor=tk.CENTER)
        self.records_tree.column("name", width=180, anchor=tk.W)
        self.records_tree.column("dept", width=180, anchor=tk.W)
        self.records_tree.column("status", width=100, anchor=tk.CENTER)
        self.records_tree.column("time", width=120, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.records_frame, 
            orient=tk.VERTICAL, 
            command=self.records_tree.yview
        )
        self.records_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        self.records_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights
        self.records_frame.grid_rowconfigure(0, weight=1)
        self.records_frame.grid_columnconfigure(0, weight=1)
        
        # Add right-click context menu
        self.setup_treeview_context_menu()
    
    def setup_treeview_context_menu(self):
        """Add a context menu to the treeview for record operations"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(
            label="Delete Selected", 
            command=self.delete_selected_records
        )
        self.context_menu.add_command(
            label="Edit Selected", 
            command=self.edit_selected_record
        )
        
        # Bind right-click event
        self.records_tree.bind(
            "<Button-3>", 
            lambda event: self.show_context_menu(event)
        )
    
    def show_context_menu(self, event):
        """Show the context menu on right-click"""
        item = self.records_tree.identify_row(event.y)
        if item:
            self.records_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def delete_selected_records(self):
        """Delete selected records from the treeview and CSV"""
        selected_items = self.records_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select records to delete")
            return
            
        confirm = messagebox.askyesno(
            "Confirm Deletion", 
            f"Delete {len(selected_items)} selected record(s)?"
        )
        
        if confirm:
            # Delete from treeview
            for item in selected_items:
                self.records_tree.delete(item)
            
            # Rewrite CSV file
            self.rewrite_csv_file()
            
            messagebox.showinfo(
                "Success", 
                f"Deleted {len(selected_items)} record(s)"
            )
    
    def edit_selected_record(self):
        """Edit the selected record"""
        selected_item = self.records_tree.selection()
        if not selected_item or len(selected_item) > 1:
            messagebox.showwarning(
                "Invalid Selection", 
                "Please select a single record to edit"
            )
            return
            
        # Get record data
        item_data = self.records_tree.item(selected_item[0])['values']
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Record")
        edit_window.geometry("400x300")
        edit_window.resizable(False, False)
        
        # Center the window
        self.center_window(edit_window)
        
        # Edit form
        ttk.Label(edit_window, text="Student ID:").pack(pady=(10, 0))
        id_entry = ttk.Entry(edit_window)
        id_entry.pack(fill=tk.X, padx=20, pady=5)
        id_entry.insert(0, item_data[0])
        
        ttk.Label(edit_window, text="Student Name:").pack()
        name_entry = ttk.Entry(edit_window)
        name_entry.pack(fill=tk.X, padx=20, pady=5)
        name_entry.insert(0, item_data[1])
        
        ttk.Label(edit_window, text="Department:").pack()
        dept_entry = ttk.Entry(edit_window)
        dept_entry.pack(fill=tk.X, padx=20, pady=5)
        dept_entry.insert(0, item_data[2])
        
        ttk.Label(edit_window, text="Status:").pack()
        status_var = tk.StringVar(value=item_data[3])
        status_combobox = ttk.Combobox(
            edit_window, 
            textvariable=status_var,
            values=["Present", "Absent", "Late"],
            state="readonly"
        )
        status_combobox.pack(fill=tk.X, padx=20, pady=5)
        
        # Save button
        save_button = ttk.Button(
            edit_window, 
            text="Save Changes",
            command=lambda: self.save_edited_record(
                selected_item[0],
                id_entry.get(),
                name_entry.get(),
                dept_entry.get(),
                status_var.get(),
                edit_window
            )
        )
        save_button.pack(pady=10)
    
    def save_edited_record(self, item, student_id, student_name, department, status, window):
        """Save the edited record"""
        if not student_id or not student_name:
            messagebox.showwarning("Input Error", "Student ID and Name are required!")
            return
            
        # Update treeview
        self.records_tree.item(
            item, 
            values=(student_id, student_name, department, status, datetime.now().strftime("%H:%M:%S"))
        )
        # Rewrite CSV file
        self.rewrite_csv_file()
        
        # Close edit window
        window.destroy()
        
        messagebox.showinfo("Success", "Record updated successfully!")
    
    def rewrite_csv_file(self):
        """Rewrite the entire CSV file with current treeview data"""
        try:
            with open(self.csv_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Student ID", "Name", "Department", "Status", "Time"])
                
                for child in self.records_tree.get_children():
                    writer.writerow(self.records_tree.item(child)["values"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes:\n{str(e)}")
    
    def submit_attendance(self):
        """Submit a new attendance record"""
        student_id = self.id_entry.get().strip()
        student_name = self.name_entry.get().strip()
        department = self.dept_entry.get().strip()
        status = self.status_var.get()
        
        # Validate input
        if not student_id or not student_name:
            messagebox.showwarning(
                "Input Error", 
                "Student ID and Name are required!"
            )
            return
        
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Add to treeview
        self.records_tree.insert(
            "", 
            tk.END, 
            values=(student_id, student_name, department, status, current_time)
        )
        
        # Save to CSV
        self.save_to_csv(student_id, student_name, department, status, current_time)
        
        # Clear input fields
        self.clear_fields()
        
        # Show success message
        messagebox.showinfo(
            "Success", 
            f"Attendance recorded for {student_name} ({student_id})"
        )
    
    def save_to_csv(self, student_id, student_name, department, status, time):
        """Save a record to the CSV file"""
        file_exists = os.path.isfile(self.csv_file)
        
        with open(self.csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            
            # Write header if file doesn't exist
            if not file_exists:
                writer.writerow(["Student ID", "Name", "Department", "Status", "Time"])
            
            writer.writerow([student_id, student_name, department, status, time])
    
    def load_records(self):
        """Load records from CSV file into the treeview"""
        if not os.path.isfile(self.csv_file):
            return
        
        self.records_tree.delete(*self.records_tree.get_children())
        
        with open(self.csv_file, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            
            for row in reader:
                if len(row) == 5:  # Ensure correct number of columns
                    self.records_tree.insert(
                        "", 
                        tk.END, 
                        values=(row[0], row[1], row[2], row[3], row[4])
                    )
    
    def view_records(self):
        """Open a window to view all records with search functionality"""
        if not self.records_tree.get_children():
            messagebox.showinfo(
                "Information", 
                "No attendance records found for today."
            )
            return
        
        # Create view window
        view_window = tk.Toplevel(self.root)
        view_window.title("Attendance Records View")
        view_window.geometry("800x500")
        self.center_window(view_window)
        
        # Search frame
        search_frame = ttk.Frame(view_window, padding="10")
        search_frame.pack(fill=tk.X)
        
        # Search components
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(
            search_frame, 
            textvariable=self.search_var, 
            width=40
        )
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        search_entry.bind("<KeyRelease>", lambda e: self.search_records(view_window))
        
        # Clear button
        clear_button = ttk.Button(
            search_frame, 
            text="Clear", 
            command=lambda: self.clear_search(view_window)
        )
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Records treeview
        columns = ("id", "name", "dept", "status", "time")
        self.view_tree = ttk.Treeview(
            view_window, 
            columns=columns, 
            show="headings",
            selectmode="extended"
        )
        
        # Configure headings
        self.view_tree.heading("id", text="Student ID", anchor=tk.CENTER)
        self.view_tree.heading("name", text="Name", anchor=tk.W)
        self.view_tree.heading("dept", text="Department", anchor=tk.W)
        self.view_tree.heading("status", text="Status", anchor=tk.CENTER)
        self.view_tree.heading("time", text="Time", anchor=tk.CENTER)
        
        # Configure columns
        self.view_tree.column("id", width=120, anchor=tk.CENTER)
        self.view_tree.column("name", width=180, anchor=tk.W)
        self.view_tree.column("dept", width=180, anchor=tk.W)
        self.view_tree.column("status", width=100, anchor=tk.CENTER)
        self.view_tree.column("time", width=120, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            view_window, 
            orient=tk.VERTICAL, 
            command=self.view_tree.yview
        )
        self.view_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack components
        self.view_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load all records initially
        self.clear_search(view_window)
    
    def clear_search(self, view_window):
        """Clear search results and show all records"""
        self.search_var.set("")
        self.view_tree.delete(*self.view_tree.get_children())
        
        for child in self.records_tree.get_children():
            values = self.records_tree.item(child)["values"]
            self.view_tree.insert("", tk.END, values=values)
    
    def search_records(self, view_window):
        """Search records based on search term"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.clear_search(view_window)
            return
            
        self.view_tree.delete(*self.view_tree.get_children())
        
        for child in self.records_tree.get_children():
            values = self.records_tree.item(child)["values"]
            
            if (search_term in str(values[0]).lower() or  
                search_term in str(values[1]).lower() or  
                search_term in str(values[2]).lower() or  
                search_term in str(values[3]).lower()):   
                
                self.view_tree.insert("", tk.END, values=values)
        
        if not self.view_tree.get_children():
            messagebox.showinfo("Search Results", "No matches found.")
    
    def export_to_csv(self):
        """Export records to CSV file"""
        if not self.records_tree.get_children():
            messagebox.showwarning(
                "Export Error", 
                "No attendance records to export!"
            )
            return
            
        try:
            with open(self.csv_file, "w", newline="") as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(["Student ID", "Name", "Department", "Status", "Time"])
                
                # Write records
                for child in self.records_tree.get_children():
                    writer.writerow(self.records_tree.item(child)["values"])
            
            messagebox.showinfo(
                "Export Successful", 
                f"Attendance records successfully exported to:\n{self.csv_file}"
            )
        except Exception as e:
            messagebox.showerror(
                "Export Error", 
                f"An error occurred while exporting:\n{str(e)}"
            )
    
    def clear_fields(self):
        """Clear all input fields"""
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.dept_entry.delete(0, tk.END)
        self.status_var.set("Present")
        self.id_entry.focus_set()
    
    def center_window(self, window):
        """Center a window on the screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop()