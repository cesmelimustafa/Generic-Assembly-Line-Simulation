import os
import pandas as pd

def run_simulation():
    print("=" * 60)
    print(" GENERIC ASSEMBLY LINE PRODUCTION SIMULATION ")
    print("=" * 60)

    # Operator count input
    while True:
        try:
            op_count = int(input("Enter the number of operators: "))
            if op_count < 2:
                print("Warning: Assembly Line A operations require at least 2 operators! Please try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    # Assembly Line A order count
    while True:
        try:
            line_a_order_count = int(input("How many 'Assembly Line A' orders will be processed?: "))
            if line_a_order_count < 0:
                print("Please enter 0 or a larger number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    # Assembly Line B order count
    while True:
        try:
            line_b_order_count = int(input("How many 'Assembly Line B' orders will be processed?: "))
            if line_b_order_count < 0:
                print("Please enter 0 or a larger number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    if line_a_order_count == 0 and line_b_order_count == 0:
        print("Warning: No orders entered. Program is terminating.")
        input("\nPress Enter to exit.")
        return

    orders_data = []

    # 1. Data Entry for Assembly Line A
    for i in range(1, line_a_order_count + 1):
        while True:
            print(f"\n--- [Line A] Enter Product Quantities for Order {i} ---")
            try:
                prod_a_count = int(input("Product A quantity: ") or "0")
                prod_b_count = int(input("Product B quantity: ") or "0")
                prod_c_count = int(input("Product C quantity: ") or "0")
                prod_d_count = int(input("Product D quantity: ") or "0")
                prod_e_count = int(input("Product E quantity: ") or "0")
                prod_f_count = int(input("Product F quantity: ") or "0")
            except ValueError:
                print("Please enter numeric values.")
                continue

            total_units = prod_a_count + prod_b_count + prod_c_count + prod_d_count + prod_e_count + prod_f_count
            if total_units <= 2:
                print("Warning: Total units for Line A must be greater than 2! Please re-enter the quantities.")
                continue

            orders_data.append({
                "type": "Line_A",
                "index": i,
                "prod_a": prod_a_count,
                "prod_b": prod_b_count,
                "prod_c": prod_c_count,
                "prod_d": prod_d_count,
                "prod_e": prod_e_count,
                "prod_f": prod_f_count,
                "total": total_units,
                "side_covers": 0  # Standard for Line A
            })
            break

    # 2. Data Entry for Assembly Line B
    for i in range(1, line_b_order_count + 1):
        while True:
            print(f"\n--- [Line B] Enter Product Quantities for Order {i} ---")
            try:
                prod_a_count = int(input("Product A quantity: ") or "0")
                prod_b_count = int(input("Product B quantity: ") or "0")
                prod_c_count = int(input("Product C quantity: ") or "0")
                prod_d_count = int(input("Product D quantity: ") or "0")
                prod_e_count = int(input("Product E quantity: ") or "0")
                prod_f_count = int(input("Product F quantity: ") or "0")

                total_units = prod_a_count + prod_b_count + prod_c_count + prod_d_count + prod_e_count + prod_f_count
                if total_units < 1:
                    print("Warning: There must be at least 1 unit in the order!")
                    continue

                side_covers = int(input("Enter the total number of side covers for this order: ") or "0")

            except ValueError:
                print("Please enter numeric values.")
                continue

            orders_data.append({
                "type": "Line_B",
                "index": i,
                "prod_a": prod_a_count,
                "prod_b": prod_b_count,
                "prod_c": prod_c_count,
                "prod_d": prod_d_count,
                "prod_e": prod_e_count,
                "prod_f": prod_f_count,
                "total": total_units,
                "side_covers": side_covers
            })
            break

    summary_data = []
    total_operator_load = {i: 0.0 for i in range(op_count)}
    total_operator_idle = {i: 0.0 for i in range(op_count)}
    grand_total_makespan = 0.0

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    excel_file = os.path.join(desktop_path, "Production_Simulation_Report.xlsx")

    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        for data in orders_data:
            order_type = data["type"]
            order_idx = data["index"]
            prod_a = data["prod_a"]
            prod_b = data["prod_b"]
            prod_d = data["prod_d"]
            prod_e = data["prod_e"]
            total_units = data["total"]
            side_covers = data["side_covers"]

            sum_a_b = prod_a + prod_b
            sum_a_b_d_e = prod_a + prod_b + prod_d + prod_e

            op_timelines = {i: 0.0 for i in range(op_count)}
            op_load = {i: 0.0 for i in range(op_count)}
            op_idle = {i: 0.0 for i in range(op_count)}
            task_logs = []

            def log_task(op_id, task_name, duration, start, end):
                task_logs.append({
                    "Operator": f"Operator {op_id + 1}",
                    "Task": task_name,
                    "Duration (min)": round(duration, 2),
                    "Start": round(start, 2),
                    "End": round(end, 2)
                })

            def assign_single_task(duration, task_name):
                op = min(op_timelines, key=op_timelines.get)
                start_time = op_timelines[op]
                end_time = start_time + duration
                op_timelines[op] = end_time
                op_load[op] += duration
                log_task(op, task_name, duration, start_time, end_time)
                return op, start_time, end_time

            def assign_joint_task_no_wait(duration, task_name):
                effective_duration = duration / 2.0
                sorted_ops = sorted(op_timelines, key=op_timelines.get)
                op1, op2 = sorted_ops[0], sorted_ops[1]
                start1, start2 = op_timelines[op1], op_timelines[op2]
                end1, end2 = start1 + effective_duration, start2 + effective_duration

                op_timelines[op1], op_timelines[op2] = end1, end2
                op_load[op1] += effective_duration
                op_load[op2] += effective_duration

                log_task(op1, f"{task_name} (Joint-Async)", effective_duration, start1, end1)
                log_task(op2, f"{task_name} (Joint-Async)", effective_duration, start2, end2)
                return (op1, op2), (start1, start2), (end1, end2)

            def assign_joint_task_with_wait(duration, task_name, full_duration_both=False):
                effective_duration = duration if full_duration_both else (duration / 2.0)
                sorted_ops = sorted(op_timelines, key=op_timelines.get)
                op1, op2 = sorted_ops[0], sorted_ops[1]

                if full_duration_both:
                    start1, start2 = op_timelines[op1], op_timelines[op2]
                    end1, end2 = start1 + effective_duration, start2 + effective_duration
                    op_timelines[op1], op_timelines[op2] = end1, end2
                    op_load[op1] += effective_duration
                    op_load[op2] += effective_duration
                    log_task(op1, f"{task_name} (Joint-Async)", effective_duration, start1, end1)
                    log_task(op2, f"{task_name} (Joint-Async)", effective_duration, start2, end2)
                    return (op1, op2), (start1, start2), (end1, end2)
                else:
                    start_time = max(op_timelines[op1], op_timelines[op2])
                    if start_time > op_timelines[op1]:
                        op_idle[op1] += (start_time - op_timelines[op1])
                        log_task(op1, "Idle Wait", start_time - op_timelines[op1], op_timelines[op1], start_time)
                    if start_time > op_timelines[op2]:
                        op_idle[op2] += (start_time - op_timelines[op2])
                        log_task(op2, "Idle Wait", start_time - op_timelines[op2], op_timelines[op2], start_time)

                    end_time = start_time + effective_duration
                    op_timelines[op1], op_timelines[op2] = end_time, end_time
                    op_load[op1] += effective_duration
                    op_load[op2] += effective_duration

                    log_task(op1, f"{task_name} (Joint-Sync)", effective_duration, start_time, end_time)
                    log_task(op2, f"{task_name} (Joint-Sync)", effective_duration, start_time, end_time)
                    return (op1, op2), start_time, end_time

            # ==========================================
            # ASSEMBLY LINE A SIMULATION (Standard Times)
            # ==========================================
            if order_type == "Line_A":
                assign_single_task(0.5, "Prep Cleaning Station")

                for _ in range(total_units):
                    assign_single_task(3.0, "Fetch Unit")

                for _ in range(total_units - 1):
                    assign_single_task(1.0, "Clean Unit")
                    assign_single_task(0.5, "Prep Fasteners")
                    assign_joint_task_no_wait(2.5, "Insert Fasteners")
                    assign_single_task(2.0, "Align Unit")
                    assign_single_task(0.5, "Prep Bolts")
                    assign_joint_task_with_wait(12.0, "Join Units", full_duration_both=True)

                assign_single_task(1.5, "Fetch Busbar")

                for _ in range(total_units - 1):
                    assign_joint_task_no_wait(2.5, "Assemble Busbar")

                for op in range(op_count):
                    start = op_timelines[op]
                    op_timelines[op] += 3.0
                    op_load[op] += 3.0
                    log_task(op, "Operator Rest Break", 3.0, start, op_timelines[op])

                for _ in range(total_units - 1):
                    assign_single_task(0.2, "Prep Copper Core")
                    assign_single_task(0.7, "Assemble Copper Core")

                assign_single_task(1.0, "Prep Side Cover Materials")
                assign_joint_task_with_wait(3.0, "Assemble Top Side Cover")

                for _ in range(sum_a_b_d_e):
                    assign_single_task(0.5, "Prep Cable Bolts")
                    assign_single_task(1.0, "Assemble Cable Bolts")

                for _ in range(total_units):
                    assign_single_task(0.5, "Prep Back Cover Materials")

                assign_joint_task_with_wait(3.5 * total_units, "Assemble Back Cover")

                for _ in range(sum_a_b):
                    assign_single_task(1.0, "Prep Hood Materials")
                    assign_single_task(4.0, "Assemble Hood")

                assign_single_task(1.0, "Prep Unit Label")
                assign_single_task(1.5, "Attach Unit Label")

                for op in range(op_count):
                    start = op_timelines[op]
                    op_timelines[op] += 2.0
                    op_load[op] += 2.0
                    log_task(op, "Operator Rest Break", 2.0, start, op_timelines[op])

            # ==========================================
            # ASSEMBLY LINE B SIMULATION (Standard Times)
            # ==========================================
            elif order_type == "Line_B":
                assign_single_task(0.5, "Prep Cleaning Station")

                for _ in range(total_units):
                    assign_single_task(3.0, "Fetch Unit")
                    assign_single_task(1.0, "Clean Unit")
                    assign_single_task(1.0, "Prep Pallet Assembly Materials")
                    assign_single_task(2.0, "Assemble Pallet")

                if side_covers > 0:
                    cover_multiplier = side_covers / 2.0
                    assign_single_task(0.8 * cover_multiplier, "Prep Side Cover Materials")
                    assign_joint_task_with_wait(2.8 * cover_multiplier, "Assemble Top Side Cover")

                for _ in range(sum_a_b_d_e):
                    assign_single_task(0.5, "Prep Cable Bolts")
                    assign_single_task(1.0, "Assemble Cable Bolts")

                for _ in range(total_units):
                    assign_single_task(0.5, "Prep Back Cover Materials")

                assign_joint_task_with_wait(3.5 * total_units, "Assemble Back Cover")

                for _ in range(sum_a_b):
                    assign_single_task(1.0, "Prep Hood Materials")
                    assign_single_task(4.0, "Assemble Hood")

                assign_single_task(1.5, "Fetch Busbar Module")

                for _ in range(total_units):
                    assign_single_task(0.7, "Prep Unit Label")
                    assign_single_task(1.0, "Attach Unit Label")
                    assign_single_task(0.5, "Prep Packaging Kit")
                    assign_single_task(1.0, "Prep Wrapping Material")
                    assign_single_task(1.8, "Wrap Unit")

                for op in range(op_count):
                    start = op_timelines[op]
                    op_timelines[op] += 2.0
                    op_load[op] += 2.0
                    log_task(op, "Operator Rest Break", 2.0, start, op_timelines[op])

            # --- Order Reporting & Summary Aggregation ---
            max_cycle_time = max(op_timelines.values())
            grand_total_makespan += max_cycle_time
            sheet_name = f"{order_type}_Order_{order_idx}"

            df_order = pd.DataFrame(task_logs)
            df_order = df_order.sort_values(by="Start").reset_index(drop=True)
            df_order.to_excel(writer, sheet_name=sheet_name, index=False)

            for op in range(op_count):
                total_operator_load[op] += op_load[op]
                total_operator_idle[op] += op_idle[op]
                summary_data.append({
                    "Order Type": "Assembly Line A" if order_type == "Line_A" else "Assembly Line B",
                    "Order No": order_idx,
                    "Operator": f"Operator {op + 1}",
                    "Total Workload (min)": round(op_load[op], 2),
                    "Idle Wait Time (min)": round(op_idle[op], 2),
                    "Order Cycle Time (Makespan)": round(max_cycle_time, 2)
                })

        # General Summary Table
        for op in range(op_count):
            summary_data.append({
                "Order Type": "GENERAL",
                "Order No": "TOTAL",
                "Operator": f"Operator {op + 1}",
                "Total Workload (min)": round(total_operator_load[op], 2),
                "Idle Wait Time (min)": round(total_operator_idle[op], 2),
                "Total Production Makespan (min)": round(grand_total_makespan, 2)
            })

        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name="General_Summary", index=False)

    print(f"\n[Success] All order reports and cumulative summaries saved to Excel:\n{excel_file}")
    input("\nProcess completed. Press Enter to exit.")

if __name__ == '__main__':
    run_simulation()