#!/usr/bin/env python3

def get_status_color(status):
    """Get the color for a given status."""
    status_colors = {
        'Pending': 'orange',
        'In Progress': 'green', 
        'On Hold': 'grey',
        'Completed': 'orange'
    }
    return status_colors.get(status, 'blue')  # default to blue if status not found

# Test the color function
if __name__ == "__main__":
    test_statuses = ['Pending', 'In Progress', 'On Hold', 'Completed', 'Unknown']
    
    print("Testing status color function:")
    print("-" * 40)
    
    for status in test_statuses:
        color = get_status_color(status)
        print(f"Status: {status:12} -> Color: {color}")
    
    print("-" * 40)
    print("Color coding has been successfully implemented!") 