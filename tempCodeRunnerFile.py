if (new_x or new_y )> grid_size or (new_x or new_y) < 0:
                            print("buiten kut")
                            break
                        elif lijst1[grid_lijst(new_x, new_y)] == speler:
                            break
                        elif lijst1[grid_lijst(new_x, new_y)] == 0:
                            lege_plaatsen.add((new_x, new_y))
                            break