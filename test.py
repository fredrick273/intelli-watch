import subprocess

def get_installed_software_with_date():
    installed_software_with_date = []
    try:
        result = subprocess.check_output(["wmic", "product", "get", "name,installdate"]).decode("utf-8")
        lines = result.strip().split("\n")
        header = [s.strip() for s in lines[0].split()]
        for line in lines[1:]:
            values = [s.strip() for s in line.split(None, len(header) - 1)]
            if len(values) == len(header):
                software_info = dict(zip(header, values))
                installed_software_with_date.append(software_info)
    except subprocess.CalledProcessError:
        pass
    return installed_software_with_date

print(get_installed_software_with_date())