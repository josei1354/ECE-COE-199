def error_increment_bool(bool_truth,bool_output,type_dict):
    if(bool_truth and bool_output):
        type_dict["TP"] += 1
    elif(bool_truth and not bool_output):
        type_dict["FN"] += 1
    elif(not bool_truth and bool_output):
        type_dict["FP"] += 1
    elif(not bool_truth and not bool_output):
        type_dict["TN"] += 1

def main_solve_error_rate(output_dict,truth_dict):
    checkbox_counts = {"TP":0, "TN":0,"FP":0,"FN":0}
    encirclement_counts = {"TP":0, "TN":0,"FP":0,"FN":0}
    for key in output_dict.keys():
        output_member = output_dict[key] 
        truth_member = truth_dict[key]
        # this is a list ex ["Checkbox", True] ex ["TX","None Yet"]
        
        data_type = output_member[0] # should also be the same as truth_member
        
        if(data_type == "Checkbox"):
            bool_truth = truth_member[1]
            bool_output = output_member[1]
            error_increment_bool(bool_truth,bool_output,checkbox_counts)
        elif(data_type == "Encirclement"):
            bool_truth = truth_member[1]
            bool_output = output_member[1]
            error_increment_bool(bool_truth,bool_output,encirclement_counts)
        elif(data_type == "TX"):
            pass

    return checkbox_counts, encirclement_counts
