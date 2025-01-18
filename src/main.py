from textnode import TextNode, TextType 
import os
import shutil

def is_dir(prefix, file):
    return not os.path.isfile(os.path.join(prefix, file))

# like shutil.copytree, but mine
def copy_tree(src_path, dst_path):
    if os.path.exists(dst_path):
        # clean out the dst_path
        print(f"Clearing {dst_path}")
        shutil.rmtree(dst_path)

    # make a new dst path
    print(f"Making {dst_path}")
    os.mkdir(dst_path)

    for item in os.listdir(src_path):
        if is_dir(src_path, item):
            print(f"Found a directory @ {os.path.join(src_path, item)}, recursing")
            copy_tree(os.path.join(src_path, item), os.path.join(dst_path, item))
        else:
            print(
                f"Found file @ {os.path.join(src_path, item)}, copying to {os.path.join(dst_path, item)}")
            shutil.copy(os.path.join(src_path, item), 
                        os.path.join(dst_path, item))

    print(f"Done")


def main():
    node = TextNode("This is a text node", TextType.BoldText, "https://www.boot.dev")

    print(node)

    copy_tree("./static", "./public")


if __name__ == "__main__":
    main()
