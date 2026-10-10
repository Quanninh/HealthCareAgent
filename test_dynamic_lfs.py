def mock_labeling_function(name=None):
    def decorator(f):
        if name:
            f.__name__ = name
        return f
    return decorator

def make_lfs_for_disease(disease_name):
    sanitized_name = disease_name.lower().replace('-', '_').replace(' ', '_')
    
    @mock_labeling_function(name=f"lf_{sanitized_name}_hallmarks")
    def lf_hallmarks(x):
        return 1
        
    @mock_labeling_function(name=f"lf_{sanitized_name}_lab_confirmation")
    def lf_lab(x):
        return 1
        
    @mock_labeling_function(name=f"lf_{sanitized_name}_negative_test")
    def lf_neg(x):
        return 0
        
    return [lf_hallmarks, lf_lab, lf_neg]

lfs = make_lfs_for_disease("COVID-19")
print([lf.__name__ for lf in lfs])
