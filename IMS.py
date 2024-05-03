from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

class Part:
    def __init__(self):
        self.last_updated_date = datetime.now()

    def update_inventory(self):
        self.last_updated_date = datetime.now()

    def __str__(self):
        return f"Last Updated Date: {self.last_updated_date}"


class Resistor(Part):
    def __init__(self, resistance, tolerance):
        super().__init__()
        if not isinstance(resistance, int):
            raise TypeError("Resistance must be an integer")
        if not isinstance(tolerance, int):
            raise TypeError("Tolerance must be an integer")

        self.resistance = resistance
        self.tolerance = tolerance

    def get_unique_characteristics(self):
        return {"resistance": self.resistance, "tolerance": self.tolerance}

    def __str__(self):
        return f"Resistance: {self.resistance} ohms, Tolerance: {self.tolerance}%, Last Updated Date: {self.last_updated_date}"


class Solder(Part):
    class Type:
        LEAD = "lead"
        LEAD_FREE = "lead-free"
        ROSIN_CORE = "rosin-core"
        ACID_CORE = "acid-core"

    def __init__(self, solder_type, length):
        super().__init__()
        if solder_type not in [Solder.Type.LEAD, Solder.Type.LEAD_FREE, Solder.Type.ROSIN_CORE, Solder.Type.ACID_CORE]:
            raise ValueError("Invalid solder type")
        self.solder_type = solder_type
        self.length = length

    def get_unique_characteristics(self):
        return {"solder_type": self.solder_type, "length": self.length}

    def __str__(self):
        return f"Solder Type: {self.solder_type}, Length: {self.length} ft, , Last Updated Date: {self.last_updated_date}"


class Wire(Part):
    def __init__(self, gauge, length):
        super().__init__()
        if not isinstance(gauge, float):
            raise TypeError("Gauge must be a floating-point number")
        if not isinstance(length, float):
            raise TypeError("Length must be a floating-point number")
        self.gauge = gauge
        self.length = length

    def get_unique_characteristics(self):
        return {"gauge": self.gauge, "length": self.length}

    def __str__(self):
        return f"Wire Gauge: {self.gauge} in, Length: {self.length} ft, , Last Updated Date: {self.last_updated_date}"


class DisplayCable(Part):
    class Type:
        HDMI = "hdmi"
        VGA = "vga"
        DISPLAYPORT = "displayport"
        MICRO_HDMI = "micro-hdmi"

    def __init__(self, cable_type, length, color):
        super().__init__()
        if cable_type not in [DisplayCable.Type.HDMI, DisplayCable.Type.VGA, DisplayCable.Type.DISPLAYPORT,
                              DisplayCable.Type.MICRO_HDMI]:
            raise ValueError("Invalid cable type")
        if not isinstance(length, float):
            raise TypeError("Length must be a floating-point number")
        self.cable_type = cable_type
        self.length = length
        self.color = color

    def get_unique_characteristics(self):
        return {"cable_type": self.cable_type, "length": self.length, "color": self.color}

    def __str__(self):
        return f"Cable Type: {self.cable_type}, Length: {self.length} ft, Color: {self.color}, Last Updated Date: {self.last_updated_date}"


class EthernetCable(Part):
    class AlphaType:
        MALE = "male"
        FEMALE = "female"

    class BetaType:
        MALE = "male"
        FEMALE = "female"

    class Speed:
        SPEED_10MBPS = "10mbps"
        SPEED_100MBPS = "100mbps"
        SPEED_1GBPS = "1gbps"

    def __init__(self, alpha_type, beta_type, speed, length):
        super().__init__()
        if alpha_type not in [EthernetCable.AlphaType.MALE, EthernetCable.AlphaType.FEMALE]:
            raise ValueError("Invalid alpha type")
        if beta_type not in [EthernetCable.BetaType.MALE, EthernetCable.BetaType.FEMALE]:
            raise ValueError("Invalid beta type")
        if speed not in [EthernetCable.Speed.SPEED_10MBPS, EthernetCable.Speed.SPEED_100MBPS,
                         EthernetCable.Speed.SPEED_1GBPS]:
            raise ValueError("Invalid speed")
        if not isinstance(length, float):
            raise TypeError("Length must be a floating-point number")
        self.alpha_type = alpha_type
        self.beta_type = beta_type
        self.speed = speed
        self.length = length

    def get_unique_characteristics(self):
        return {"alpha_type": self.alpha_type, "beta_type": self.beta_type, "speed": self.speed, "length": self.length}

    def __str__(self):
        return f"Alpha Type: {self.alpha_type}, Beta Type: {self.beta_type}, Speed: {self.speed}, Length: {self.length}, Last Updated Date: {self.last_updated_date}"


class Inventory:
    def __init__(self):
        self.parts_inventory = {}
        self.usage_counter = {}
        self.out_of_stock_counter = {}

    def add_part(self, part, sku):
        if not isinstance(part, Part):
            raise TypeError("Part must be a subclass of Part")

        for existing_sku, item in self.parts_inventory.items():
            existing_part = item['part']
            if (type(existing_part) == type(part) and
                    existing_part.get_unique_characteristics() == part.get_unique_characteristics()):
                quantity = int(
                    input("An item with the same characteristics already exists. Enter the quantity to add: "))
                if quantity < 0:
                    raise ValueError("Quantity cannot be negative")
                self.parts_inventory[existing_sku]['quantity'] += quantity
                self.parts_inventory[existing_sku]['part'].update_inventory()
                return

        if sku in self.parts_inventory:
            raise ValueError("SKU already exists")
        self.parts_inventory[sku] = {'part': part, 'quantity': 0}
        self.usage_counter[sku] = 0
        self.out_of_stock_counter[sku] = 0

    def add_inventory(self, sku, quantity):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if sku not in self.parts_inventory:
            raise ValueError("SKU does not exist")
        self.parts_inventory[sku]['quantity'] += quantity
        self.parts_inventory[sku]['part'].update_inventory()

    def get_quantity(self, sku):
        if sku not in self.parts_inventory:
            raise ValueError("SKU does not exist")
        return self.parts_inventory[sku]['quantity']

    def get_inventory(self):
        return self.parts_inventory

    def get_part(self, sku):
        if sku not in self.parts_inventory:
            raise ValueError("SKU does not exist")
        return self.parts_inventory[sku]['part']

    def search(self, part_class, **kwargs):
        found_parts = []
        for sku, item in self.parts_inventory.items():
            if isinstance(item['part'], part_class):
                match = True
                for key, value in kwargs.items():
                    if getattr(item['part'], key, None) != value:
                        match = False
                        break
                if match:
                    found_parts.append((sku, item['part']))
        return found_parts

    def delete_part(self, sku):
        if sku not in self.parts_inventory:
            raise ValueError("SKU does not exist")
        del self.parts_inventory[sku]

    def track_usage(self, sku):
        if sku not in self.usage_counter:
            raise ValueError("SKU does not exist in usage counter")
        self.usage_counter[sku] += 1

    def track_out_of_stock(self, sku):
        if sku not in self.out_of_stock_counter:
            raise ValueError("SKU does not exist in out of stock counter")
        self.out_of_stock_counter[sku] += 1

    def get_most_used_parts(self, n=5):
        return sorted(self.usage_counter.items(), key=lambda x: x[1], reverse=True)[:n]

    def get_most_out_of_stock_parts(self, n=5):
        return sorted(self.out_of_stock_counter.items(), key=lambda x: x[1], reverse=True)[:n]


# Interactive menu
def main_menu():
    print("Welcome to the Inventory Management System\n")
    print("1. Add Part")
    print("2. Add Inventory")
    print("3. Get Quantity")
    print("4. Get Inventory")
    print("5. Get Part")
    print("6. Search")
    print("7. Delete Part")
    print("8. Track Usage")
    print("9. Track Out of Stock")
    print("10. Most Used Parts (Graph)")
    print("11. Most Out of Stock Parts (Graph)")
    print("12. Exit")


def add_part_menu():
    print("Add Part:")
    print("1. Resistor")
    print("2. Solder")
    print("3. Wire")
    print("4. Display Cable")
    print("5. Ethernet Cable")


def get_part_characteristics(part_type):
    while True:
        characteristics = {}
        if part_type == 1:  # Resistor
            try:
                resistance = int(input("Enter Resistance (ohms): "))
                tolerance = int(input("Enter Tolerance (%): "))
                characteristics['resistance'] = resistance
                characteristics['tolerance'] = tolerance
                break
            except ValueError:
                print("Invalid input. Please enter integer values for resistance and tolerance.")
        elif part_type == 2:  # Solder
            solder_type = input("Enter Solder Type (lead, lead-free, rosin-core, acid-core): ")
            length = input("Enter Length (ft): ")
            try:
                length = float(length)
                if solder_type.lower() not in ['lead', 'lead-free', 'rosin-core', 'acid-core']:
                    raise ValueError("Invalid solder type.")
                characteristics['solder_type'] = solder_type
                characteristics['length'] = length
                break
            except ValueError as e:
                print(f"Error: {e} Please enter a valid solder type.")
        elif part_type == 3:  # Wire
            gauge = input("Enter Wire Gauge (in): ")
            length = input("Enter Length (ft): ")
            try:
                gauge = float(gauge)
                length = float(length)
                characteristics['gauge'] = gauge
                characteristics['length'] = length
                break
            except ValueError:
                print("Invalid input. Please enter floating-point values for gauge and length.")
        elif part_type == 4:  # Display Cable
            cable_type = input("Enter Cable Type (hdmi, vga, displayport, micro-hdmi): ")
            length = input("Enter Length (ft): ")
            color = input("Enter Color (hex code): ")
            try:
                length = float(length)
                if cable_type.lower() not in ['hdmi', 'vga', 'displayport', 'micro-hdmi']:
                    raise ValueError("Invalid cable type.")
                characteristics['cable_type'] = cable_type
                characteristics['length'] = length
                characteristics['color'] = color
                break
            except ValueError as e:
                print(f"Error: {e} Please enter a valid cable type.")
        elif part_type == 5:  # Ethernet Cable
            alpha_type = input("Enter Alpha Type (male, female): ")
            beta_type = input("Enter Beta Type (male, female): ")
            speed = input("Enter Speed (10mbps, 100mbps, 1gbps, 10gbps): ")
            length = input("Enter Length (ft): ")
            try:
                length = float(length)
                if alpha_type.lower() not in ['male', 'female'] or beta_type.lower() not in ['male', 'female']:
                    raise ValueError("Invalid alpha or beta type.")
                if speed.lower() not in ['10mbps', '100mbps', '1gbps', '10gbps']:
                    raise ValueError("Invalid speed.")
                characteristics['alpha_type'] = alpha_type
                characteristics['beta_type'] = beta_type
                characteristics['speed'] = speed
                characteristics['length'] = length
                break
            except ValueError as e:
                print(f"Error: {e} Please enter valid options for alpha/beta type and speed.")
        else:
            print("Invalid choice")
            break
    return characteristics



def track_usage_menu():
    sku = input("Enter SKU for the part used: ")
    try:
        inventory.track_usage(sku)
        print(f"Usage of SKU {sku} tracked successfully")
    except ValueError as e:
        print(f"Error: {e}")


def track_out_of_stock_menu():
    sku = input("Enter SKU for the part that fell out of stock: ")
    try:
        inventory.track_out_of_stock(sku)
        print(f"Out of stock occurrence of SKU {sku} tracked successfully")
    except ValueError as e:
        print(f"Error: {e}")


def plot_most_used_parts():
    most_used = inventory.get_most_used_parts()
    df = pd.DataFrame(most_used, columns=['SKU', 'Usage Count'])
    df.plot(kind='bar', x='SKU', y='Usage Count', legend=None)
    plt.title('Most Used Parts')
    plt.xlabel('SKU')
    plt.ylabel('Usage Count')
    plt.show()


def plot_most_out_of_stock_parts():
    most_out_of_stock = inventory.get_most_out_of_stock_parts()
    df = pd.DataFrame(most_out_of_stock, columns=['SKU', 'Out of Stock Count'])
    df.plot(kind='bar', x='SKU', y='Out of Stock Count', legend=None)
    plt.title('Most Out of Stock Parts')
    plt.xlabel('SKU')
    plt.ylabel('Out of Stock Count')
    plt.show()


inventory = Inventory()

while True:
    main_menu()
    choice = input("\nEnter your choice: ")

    if choice == '1':  # Add Part
        add_part_menu()
        part_type = int(input("Enter the type of part to add: "))
        characteristics = get_part_characteristics(part_type)
        try:
            if part_type == 1:
                part = Resistor(**characteristics)
            elif part_type == 2:
                part = Solder(**characteristics)
            elif part_type == 3:
                part = Wire(**characteristics)
            elif part_type == 4:
                part = DisplayCable(**characteristics)
            elif part_type == 5:
                part = EthernetCable(**characteristics)
            sku = input("Enter SKU: ")
            inventory.add_part(part, sku)
            print("Part added successfully")
        except ValueError as e:
            print(f"Error: {e}")

    elif choice == '2':  # Add Inventory
        sku = input("Enter SKU: ")
        quantity = int(input("Enter Quantity: "))
        try:
            inventory.add_inventory(sku, quantity)
            print("Inventory added successfully")
        except ValueError as e:
            print(f"Error: {e}")

    elif choice == '3':  # Get Quantity
        sku = input("Enter SKU: ")
        try:
            quantity = inventory.get_quantity(sku)
            print(f"Quantity of SKU {sku}: {quantity}")
        except ValueError as e:
            print(f"Error: {e}")

    elif choice == '4':  # Get Inventory
        inventory_list = inventory.get_inventory()
        if not inventory_list:
            print("Inventory is empty")
        else:
            print("Inventory:")
            for sku, item in inventory_list.items():
                print(f"SKU: {sku}, Quantity: {item['quantity']}, Part: {item['part']}")

    elif choice == '5':  # Get Part
        sku = input("Enter SKU: ")
        try:
            part = inventory.get_part(sku)
            print(f"Part characteristics for SKU {sku}: {part}")
        except ValueError as e:
            print(f"Error: {e}")

    elif choice == '6':  # Search
        part_class = None
        while part_class not in [Resistor, Solder, Wire, DisplayCable, EthernetCable]:
            print("Search:")
            print("1. Resistor")
            print("2. Solder")
            print("3. Wire")
            print("4. Display Cable")
            print("5. Ethernet Cable")
            part_choice = input("Enter the type of part to search: ")
            if part_choice == '1':
                part_class = Resistor
            elif part_choice == '2':
                part_class = Solder
            elif part_choice == '3':
                part_class = Wire
            elif part_choice == '4':
                part_class = DisplayCable
            elif part_choice == '5':
                part_class = EthernetCable
            else:
                print("Invalid choice")
        characteristics = {}
        if part_class == Resistor:
            resistance = input("Enter Resistance (leave blank if not required): ")
            if resistance:
                characteristics['resistance'] = int(resistance)
            tolerance = input("Enter Tolerance (leave blank if not required): ")
            if tolerance:
                characteristics['tolerance'] = int(tolerance)
        elif part_class == Solder:
            solder_type = input("Enter Solder Type (leave blank if not required): ")
            if solder_type:
                characteristics['solder_type'] = solder_type
            length = input("Enter Length (leave blank if not required): ")
            if length:
                characteristics['length'] = float(length)
        elif part_class == Wire:
            gauge = input("Enter Wire Gauge (leave blank if not required): ")
            if gauge:
                characteristics['gauge'] = float(gauge)
            length = input("Enter Length (leave blank if not required): ")
            if length:
                characteristics['length'] = float(length)
        elif part_class == DisplayCable:
            cable_type = input("Enter Cable Type (leave blank if not required): ")
            if cable_type:
                characteristics['cable_type'] = cable_type
            length = input("Enter Length (leave blank if not required): ")
            if length:
                characteristics['length'] = float(length)
            color = input("Enter Color (leave blank if not required): ")
            if color:
                characteristics['color'] = color
        elif part_class == EthernetCable:
            alpha_type = input("Enter Alpha Type (leave blank if not required): ")
            if alpha_type:
                characteristics['alpha_type'] = alpha_type
            beta_type = input("Enter Beta Type (leave blank if not required): ")
            if beta_type:
                characteristics['beta_type'] = beta_type
            speed = input("Enter Speed (leave blank if not required): ")
            if speed:
                characteristics['speed'] = speed
            length = input("Enter Length (leave blank if not required): ")
            if length:
                characteristics['length'] = float(length)
        found_parts = inventory.search(part_class, **characteristics)
        if not found_parts:
            print("No matching parts found")
        else:
            print("Matching Parts:")
            for sku, part in found_parts:
                print(f"SKU: {sku}, Part: {part}")

    elif choice == '7':  # Delete Part
        sku = input("Enter SKU: ")
        try:
            inventory.delete_part(sku)
            print(f"Part with SKU {sku} deleted successfully")
        except ValueError as e:
            print(f"Error: {e}")

    elif choice == '8':  # Track Usage
        track_usage_menu()

    elif choice == '9':  # Track Out of Stock
        track_out_of_stock_menu()

    elif choice == '10':  # Most Used Parts (Graph)
        plot_most_used_parts()

    elif choice == '11':  # Most Out of Stock Parts (Graph)
        plot_most_out_of_stock_parts()

    elif choice == '12':  # Exit
        print("Exiting...")
        break

    else:
        print("Invalid choice")

