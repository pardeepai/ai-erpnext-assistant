from app.graph.nodes import analyzer_node, reflector_node


state={'customer': 'sandeep',
 'sales_orders': {'data': [{'name': 'SAL-ORD-2026-00001',
                            'customer': 'sandeep',
                            'transaction_date': '2026-09-19',
                            'status': 'Draft'},
                           {'name': 'SAL-ORD-2026-00005',
                            'customer': 'sandeep',
                            'transaction_date': '2026-09-19',
                            'status': 'Completed'},
                           {'name': 'SAL-ORD-2026-00006',
                            'customer': 'sandeep',
                            'transaction_date': '2026-09-24',
                            'status': 'To Deliver'},
                           {'name': 'SAL-ORD-2026-00007',
                            'customer': 'sandeep',
                            'transaction_date': '2026-10-10',
                            'status': 'Cancelled'},
                           {'name': 'SAL-ORD-2026-00008',
                            'customer': 'sandeep',
                            'transaction_date': '2026-10-03',
                            'status': 'To Deliver and Bill'}]},
 'order_counts': {'total': 5,
                  'completed': 1,
                  'pending': 2,
                  'cancelled': 1,
                  'draft': 1,
                  'to_deliver': 0},
 'analysis': '',
 'reflection': '',
 'approved': False,
 'iteration': 0,
 'feedback': '',
 'lesson': '',
 'previous_attempts': []}


print("Initial state:")
print(state)

print("\n--- Analyzer Node ---")

state = analyzer_node(state)

print("Analysis:")
print(state["analysis"])
print("Iteration:", state["iteration"])

print("\n--- Reflector Node ---")

state = reflector_node(state)

print("Reflection:")
print(state["reflection"])
print("Approved:", state["approved"])