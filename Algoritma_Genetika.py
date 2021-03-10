# Muhammad Azmi / 10 maret 2021
# sumber referensi : youtube Kelas Terbuka / playlist algoritma genetika (matlab)

import random
import decimal
import os

# target = "wirosableng"
target = raw_input("Target :")
target = list(target)
besar_populasi = int(raw_input("Besar Populasi : "))
# besar_populasi = 10
laju_mutasi = float(raw_input("Laju Mutasi [0.xx - 1.00] : "))
# laju_mutasi = 0.1

# Representasi Genetik
def create_gen (panjang_gen) :  
    gen = ''.join(chr(random.randint(32,126)) for i in range(panjang_gen))
    return gen

# Fitness function
def calculate_fitness (gen, target) :
    gen = list(gen) # ubah dulu ke list agar bisa di compare
    # cari data yg sama antara GEN dan TARGET
    data_sama = 0;
    for i in range(len(target)):
        if (gen[i] == target[i]): #compare
            data_sama = data_sama + 1   # hitung, mengetahui berapa banyak karakter yg sama antara GEN dan TARGET

    # Hitung Fitness gen
    fitness = ((data_sama/decimal.Decimal(len(target)))*100)
    return fitness

# Create population
def create_population (target, besar_populasi) :
    populasi = []
    for i in range(besar_populasi):   # di ulang sebanyak besar_populasi
        penampung_for = []
        for j in range(1) :  # 2 kali diulang : gen dan fitness
            gen = list(create_gen(len(target))) # memenggil method create_gen, yg berupa kembalian huruf-huruf/GEN
            penampung_for.append(gen) 
            penampung_for.append(calculate_fitness(gen, target))
        populasi.append(penampung_for)       # append adalah Tumpok
    
    return populasi    

# Seleksi Individu Terbaik
def selection (populasi) :
    # memasukkan populasi[fitness] kedalam array 1 dimensi untuk mencari nilai max()
    fitness_data = []
    for i in range(len(populasi)):
        fitness_data.append(populasi[i][1]) #index 1 adlh value fitness

    # Parent 1
    index_fitness_data = fitness_data.index(max(fitness_data)) # mendapatkan nilai fitness tertinggi berdasakan index
    parent1_gen = populasi[index_fitness_data][0]
    parent1_fitness = populasi[index_fitness_data][1]

    # menghapus data yg menjadi parent1 didalam populasi dan juga hapus fitnes data terbaik
    populasi.remove(populasi[index_fitness_data])
    fitness_data.remove(fitness_data[index_fitness_data])

    # Parent 2
    index_fitness_data = fitness_data.index(max(fitness_data)) # mendapatkan nilai fitness tertinggi berdasakan index
    parent2_gen = populasi[index_fitness_data][0]
    parent2_fitness = populasi[index_fitness_data][1]

    #  # menghapus data yg menjadi parent2 didalam populasi dan juga hapus fitnes data terbaik
    # populasi.remove(populasi[index_fitness_data])
    # fitness_data.remove(fitness_data[index_fitness_data])

    # mengembalikan data yg dihapus tadi di atas kedalam populasi
    kembali = [parent1_gen, parent1_fitness]
    populasi.insert((len(populasi)+1), kembali)

    best1 = parent1_gen
    best2 = parent2_gen

    return best1, best2

# Crossover
def crossover (parent1, parent2) :
    child1 = parent1 # value parent1 di asigment ke child1
    child2 = parent2 # value parent2 di asigment ke child2

    #parent asal
    # print("parent 1 :", parent1)
    # print("parent 2 :", parent2)

    # crossover point (CP)
    CP = round(len(parent1)/2) # panjang gen Parent di bagi 2, CP bertipe float

    # mengawinkan silang data
    child1 = child1[0:int(CP)] + parent2[int(CP):len(parent1)] # melakukan concate child1 dan parent2
    child2 = child2[0:int(CP)] + parent1[int(CP):len(parent1)] # melakukan concate child2 dan parent1

    # anak setelah crossover
    # print("child 1 :", child1)
    # print("child 2 :", child2)

    return child1, child2

# Mutasi
def mutation(child, laju_mutasi) :
    mutant = child

    # print("Child sebelum berubah jadi Mutant : ",mutant)

    for i in range(len(mutant)):
        if random.random() <= laju_mutasi : # fungsi random() menghasilkan angka antara [0.xx sampai 1.00]
            mutant[i] = random.choice(chr(random.randint(32,126)))   # random.choice() menghasilkan karakter ascii secara acak

    # print("Child setelah berubah jadi Mutant : ",mutant)
    return mutant

# Regenerasi
def regeneration(children, populasi) :
    # ambil fitnes dari populasi awal
    fitness = []
    for i in range(len(populasi)):
        fitness.append(populasi[i][1])

    # remove individu & fitness berdasarkan fitnes minimum
    for i in range(len(children)):
        index_fitness = fitness.index(min(fitness)) # mendapatkan index minimum di list fitness
        populasi.remove(populasi[index_fitness]) # menghapus data populasi minimum tersebut
        fitness.remove(fitness[index_fitness])
        
    # add member/individu dari children
    for i in range(len(children)):
        n = len(populasi) + 1
        populasi.insert(n, children[i])

    new_populasi = populasi
    return populasi

# Check Solusi 100%
def check_solusi (populasi) :
    # ambil fitnes dari populasi untuk menentukan batas perulangan atau terminate(berhenti)
    fitness_cek = []
    for i in range(len(populasi)):
        fitness_cek.append(populasi[i][1])

    indexx = fitness_cek.index(max(fitness_cek))

    solusi = ''
    if 100 in fitness_cek : # Mengecek Apakah ada angka/fitness bernilai 100 pada list fitness_cek
        isLooping = False
        solusi = populasi[indexx][0]
        # print("INDEX :", indexx)
    else :
        isLooping = True
        solusi = populasi[indexx][0]

    return isLooping, solusi

# Logging
def logging(populasi, target, solusi, generasi) :
    print("Target   : {0} ".format(target))
    print("Solusi   : {0} ".format(solusi))
    print("Generasi : {0} ".format(generasi))

    for i in range(len(populasi)):
        gen     = populasi[i][0]
        fitness = populasi[i][1]
        print("Gen : {gen} | Fitness : {fitness}".format(gen = gen, fitness = fitness))


# Algoritma Genetika
def algoritma_genetika(target, besar_populasi, laju_mutasi) :
    # Membuat populasi
    populasi = create_population(target, besar_populasi)  # kembalian crete_population() berupa list-list gen dan fitness yg diacak-acak

    isLooping = True
    iterasi = 0
    while(isLooping) :
        # seleksi individu terbaik untuk di jadikan parent
        parent = selection(populasi) # kembalian selection() berupa [parent1],[parent2]

        #crossover / kawin silang
        child = crossover(parent[0], parent[1]) # kembalian crossover() berupa [child1],[child2]

        # mutasi
        mutant1_gen = mutation(child[0], laju_mutasi)  #isi mutant1 hanya gen
        mutant2_gen = mutation(child[1], laju_mutasi)

        # hitung fitness si Mutant
        mutant1_fitness = calculate_fitness(mutant1_gen, target) # isi mutan1_fitness cuma fitnes doang
        mutant2_fitness = calculate_fitness(mutant2_gen, target)

        # calon anggota populasi baru
        children = [[mutant1_gen, mutant1_fitness], [mutant2_gen, mutant2_fitness]]

        # regenerasi
        populasi = regeneration(children, populasi)
        iterasi = iterasi+1 # generasi

        # Check solusi
        solusi = check_solusi(populasi) # kembalian method ini berupa Kondisi [islooping dan solusi]
        isLooping = solusi[0]
        
        # hapus console
        os.system('cls') #clear console

        # logging / menampilakn proses yang berjalan
        logging(populasi, target, solusi[1], iterasi)

# Start Algoritma
# Pemanggilan Fungsi Algoritma Genetika
algoritma_genetika(target, besar_populasi, laju_mutasi)


    








