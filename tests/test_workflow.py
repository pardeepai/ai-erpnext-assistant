from app.graph.workflow import workflow


initial_state = {'customer': 'sandeep',
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


result = workflow.invoke(initial_state)


print("\n--- Final Result ---")

print("Customer:", result["customer"])
print("Iteration:", result["iteration"])

print("\nAnalysis:")
print(result["analysis"])

print("\nReflection:")
print(result["reflection"])

print("\nApproved:", result["approved"])