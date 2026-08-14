from functions.get_files_info import get_files_info

def get_the_info(t):
    if isinstance(t,str):
        print(t)
        return
    for x in t:
        print(f"{x["name"]}: file_size={x["file_size"]} bytes, is_dir={x["is_dir"]}")

t1=(get_files_info("calculator", "."))
t2=(get_files_info("calculator", "pkg"))
t3=(get_files_info("calculator", "/bin"))
t4=(get_files_info("calculator", "../"))
get_the_info(t1)
get_the_info(t2)
get_the_info(t3)
get_the_info(t4)
