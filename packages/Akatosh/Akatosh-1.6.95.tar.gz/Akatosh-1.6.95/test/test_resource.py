from Akatosh import event, Mundus, Resource

res = Resource(capacity=10)

@event(at=0, step=1, till=9)
def use_resource():
    res.get(1)
    print(f"{Mundus.now}:\tget 1 from {res.available_quantity}/{res.capacity}.")

Mundus.simulate(10)
print(res.utilization_in_past(period = 3, aggrate='AVG'))
