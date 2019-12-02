import operator

serverType = {
     "large": 1,
     "xlarge": 2,
     "2xlarge": 4,
     "4xlarge": 8,
     "8xlarge": 16,
     "10xlarge": 32
}
region = {
        "us-east": {
            "large": 0.1122,
            "xlarge": 0.23,
            "2xlarge": 0.45,
            "4xlarge": 0.774,
            "8xlarge": 1.125,
            "10xlarge": 1.82
        },
        "us-west": {
            "large": 0.14,
            "2xlarge": 0.1212,
            "4xlarge": 9.89,
            "8xlarge": 1.4,
            "10xlarge": 2.97
        },
        "us-south": {
            "large": 0.14,
            "2xlarge": 0.1212,
            "4xlarge": 9.89,
            "8xlarge": 1.4,
            "10xlarge": 2.97
        }
}


def get_costs_per_cpu(region): #the function gets costs per CPU
    y = []
    for x in region:
        for y in region[x]:
            region[x][y] = region[x][y] / serverType[y] #calculating cost per CPU by dividing no of cpus by cost of server
    #print(region)
    return (region)


def get_lowest_cpu_rate(cost_per_cpu, index=0): #finding the lowest rate instance type and its region 
    temp_dict = {}
    price = []
    instance_type = []
    map_region = []
    #print(cost_per_cpu)

    for region in cost_per_cpu:
        # sorted(cost_per_cpu[region].values())
        map_region.append(region)
        x = sorted(cost_per_cpu[region].items(), key=operator.itemgetter(1)) #sorting cost per cpu in ascending order
        #print(x)
        temp_dict.update({region: x})  # repeated
        #print(temp_dict)
    #print(temp_dict)

    for regions in temp_dict:
        try:
            instance_type.append(temp_dict[regions][index][0]) #gives lowest cost server from all regions
            price.append(temp_dict[regions][index][1]) #saving the serverType & cost in a temporary dictionary
        except IndexError:
            continue

    selected_price = min(price)
    selected_region = map_region[price.index(min(price))] #minimum among instance costs
    selected_instance_type = instance_type[price.index(min(price))] #instance type of minimum instance
    index_of_selected_region = price.index(min(price)) #saving index of lowest priced instance
    selected_vcpu = serverType[selected_instance_type]
    # print(selected_region, index_of_selected_region, selected_instance_type, selected_price, selected_vcpu)
    return selected_region, index_of_selected_region, selected_instance_type, selected_price, selected_vcpu


def get_costs(instances, hours=0, cpus=0, price=0): #calculates the optimized number of servers according to servers required or cost

    cost_per_cpu = get_costs_per_cpu(instances)
    count = 0
    response = {}
    server = {}
    price_per_region = []
    regions = []
    for region in cost_per_cpu:
        price_per_region.append(0)
        regions.append(region)

    if cpus != 0 and hours != 0 and price == 0: #when n CPUs and H hours given
        # print("if")

        while cpus > 0:
            print("inside")
            # print(count)
            selected_region, index_of_selected_region, selected_instance_type, selected_price, selected_vcpu = get_lowest_cpu_rate(cost_per_cpu, count)
            number_of_instance_taken = int(cpus / selected_vcpu) #finding number of cpus gained from selected low cost instance
            if number_of_instance_taken ==0: #when lowest cost instance has a greater number of cpus than required the count variable increments
                count += 1
                continue

            cpus = cpus % selected_vcpu
            price_per_region[index_of_selected_region] += number_of_instance_taken*selected_price*hours #finding total cost
            server[selected_instance_type] = {selected_region, number_of_instance_taken}
            #print(server)
        print(regions)
        print("Total_cost", price_per_region)
        print(server)


    if cpus == 0 and hours != 0 and price != 0: #when H hours and max price given

        selected_region, index_of_selected_region, selected_instance_type, selected_price, selected_vcpu = get_lowest_cpu_rate(
            cost_per_cpu, 0)
        final_price_single_cpu = selected_price*hours #cost of running selected instance for H hours
        no_of_affordable_cpu = int(price/final_price_single_cpu)
        print(selected_region, selected_instance_type, no_of_affordable_cpu)
get_costs(region, hours=10, price=38)
