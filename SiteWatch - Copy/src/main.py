import gui

# KEEP THIS FILE AS CLEAN AS POSSIBLE!!!
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
        gui.main()


if __name__ == "__main__":
    main()
