import datetime
import json
# from app import app, db
from app.models.Machine import Machine
from app.models.Order import Order
# from app.models.User import User
from app.models.product import Product

SHIFT_HOURS = 8

class SubPlan(object):

    def __init__(self, machine, order):
        self.machine = machine
        self.order = [order]
        self.shift_overflow = False
        self.time = SHIFT_HOURS * 60

    def to_dict(self):
        output = {}
        output['machine'] = self.machine.id
        output['order'] =  [x.id for x in self.order]
        output['shift_overflow'] = self.shift_overflow
        output['time'] = self.time
        return output


class Plan(object):
    def __init__(self):
        self.date = datetime.datetime.now()
        self.rough_plan = []

    def plan(self):
        remaining_orders = Order.query.filter(
            Order.status == 'PLANNED').order_by(Order.created_at.asc())\
            .order_by(Order.estimated_time_to_finish.desc()).all()
        machines = Machine.query.all()

        # print '\n------------'
        # print Order.query.filter(
        #     Order.status == 'PLANNED').order_by(Order.created_at.desc())
        #     .order_by(Order.estimated_time_to_finish.desc())
        # print '\n'

        print remaining_orders

        shift_time = SHIFT_HOURS * 60

        order_count = len(remaining_orders)
        machine_count = len(machines)

        order_index = machine_index = 0

        print "Order Count ", order_count
        print "Machine Count: ", machine_count
        while machine_index <= machine_count and order_index < order_count:
            print "mi: ", machine_index, "oi: ", order_index
            print "ETA: ", remaining_orders[order_index]\
                .estimated_time_to_finish
            print "Quantity: ", remaining_orders[order_index].quantity

            plan_adjusted = False
            for subplan in self.rough_plan:
                task_time = remaining_orders[order_index].estimated_time_to_finish

                if subplan.time - task_time >= 0:
                    subplan.order.append(remaining_orders[order_index])
                    subplan.time -= task_time
                    plan_adjusted = True

            if not plan_adjusted and machine_index < machine_count:
                shift_overflow = remaining_orders[order_index].estimated_time_to_finish > shift_time
                subplan = SubPlan(machines[machine_index], remaining_orders[order_index])
                subplan.shift_overflow = shift_overflow
                subplan.time -= remaining_orders[order_index].estimated_time_to_finish
                self.rough_plan.append(subplan)       
                machine_index += 1

            order_index += 1
            print 'appended plan'

        for subplan in self.rough_plan:
            print json.dumps(subplan.to_dict())

        raise Exception("\n\n\n*****************\nMethod implementation not complete!\n*****************")
