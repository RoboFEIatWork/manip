def create_matrix():
    return [-1, -1]  # Inicializa os slots vazios como uma lista


def get_pages():
    pages = [4, 5, 3, 1, 2]
    return pages


def init():
    caramelo_slots = create_matrix()
    pages = get_pages()
    order = sorted(pages)
    n = 0

    def clean_move():
        """Move o item correto para a posição ordenada."""
        index = pages.index(order[n])  # Localiza o índice do item correto
        print(f"\nMovendo {order[n]} da posição {index} para a posição {n} em pages.")
        pages[index] = -1  # Marca o campo anterior como vazio
        pages[n] = order[n]  # Move o item para a posição correta
        print(f"Estado atual de pages: {pages}")
        print(f"Estado atual de caramelo_slots: {caramelo_slots}")

    def move_from_caramelo():
        """Move itens do caramelo_slots de volta para pages."""
        for i in range(len(caramelo_slots)):
            if caramelo_slots[i] != -1:
                item = caramelo_slots[i]
                if item == order[n]:
                    print(f"\nMovendo {item} de caramelo_slots[{i}] para pages[{n}].")
                    pages[n] = item
                    caramelo_slots[i] = -1  # Marca o slot como vazio
                    print(f"Estado atual de caramelo_slots: {caramelo_slots}")
                    print(f"Estado atual de pages: {pages}")
                    return

    def move_to_caramelo():
        """Move itens incorretos de pages para caramelo_slots."""
        for i in range(len(caramelo_slots)):
            if caramelo_slots[i] == -1 and pages[n] != -1:
                print(f"\nMovendo {pages[n]} de pages[{n}] para caramelo_slots[{i}].")
                caramelo_slots[i] = pages[n]
                pages[n] = -1  # Marca a posição em pages como vazia
                print(f"Estado atual de caramelo_slots: {caramelo_slots}")
                print(f"Estado atual de pages: {pages}")
                break

    while pages != order:
        print(f"\nEstado atual de pages antes da ação: {pages}")
        print(f"Estado atual de caramelo_slots antes da ação: {caramelo_slots}")
        
        if pages[n] != order[n]:
            move_to_caramelo()
            if order[n] in pages:
                clean_move()
            else:
                move_from_caramelo()
        else:
            n += 1
            if n >= len(pages):
                break


    print("\nOrdenação concluída.")
    print(f"Estado final de pages: {pages}")
    print(f"Estado final de caramelo_slots: {caramelo_slots}")
    return pages


# Executa o código
print(init())  # Saída esperada: [1, 2, 3, 4, 5]
