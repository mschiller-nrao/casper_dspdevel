from vunit import VUnit
from itertools import product
from random import choice
from random import choices
from random import sample
import glob
import os
# Create VUnit instance by parsing command line arguments
vu = VUnit.from_argv()

def get_ranges(dat_w,margin):
    min_val = -(2**(dat_w-1))
    max_val = (-min_val)-1
    ab_value_ranges = [
        (min_val,min_val+margin,-margin,margin-1),
        (-margin,+margin,-margin,margin-1),
        (max_val,max_val-margin,-margin,margin-1)
        ]
    return ab_value_ranges

def generate_tests(obj, in_dat_w, inp_pipeline,product_pipeline, out_pipeline, conjugate_b=None, adder_pipeline=None):
    """
    Generate test by varying the generics of common_counter:
        in_dat_w : int {4,5,6,7,8}
        conjugate_b : int {TRUE,FALSE}
        out_dat_w : int {2*in_dat_w}
        out_pipeline : >=0
        inp_pipeline : {0,1}
        adder_pipeline : {0,1}
        product_pipeline : {0,1}
    """
    if not conjugate_b:
        for i_d_w in in_dat_w:
            margin = 16
            ab_value_ranges = get_ranges(i_d_w,margin)
            ab_value_ranges = choices(ab_value_ranges, k=2)
            for a_v_min, a_v_max, b_v_min, b_v_max in ab_value_ranges:
                value_range_string = ", a_val = [%d, %d] , b_val = [%d, %d]" % (a_v_min, a_v_max,b_v_min,b_v_max)
                config_name = "i_d_w=%i, o_d_w=%i, inp_pipeline=%i, out_pipeline=%i, prod_pipe=%i" % (i_d_w, 2 * i_d_w + 1, inp_pipeline, out_pipeline, product_pipeline) +\
                                value_range_string
                obj.add_config(
                    name = config_name,
                    generics=dict(g_in_dat_w=i_d_w, g_out_dat_w=2*i_d_w + 1, g_pipeline_input=inp_pipeline, g_pipeline_product=product_pipeline,
                    g_pipeline_output=out_pipeline, g_a_val_min=a_v_min, g_a_val_max=a_v_max, g_b_val_min=b_v_min, g_b_val_max=b_v_max)
                )
    else:
        for i_d_w, conj_b in product(in_dat_w,conjugate_b):
            margin = 16
            ab_value_ranges = get_ranges(i_d_w,margin)
            a_v_min, a_v_max, b_v_min, b_v_max = choice(ab_value_ranges)
            config_name = "i_d_w=%i, o_d_w=%i, conj_b=%i, inp_pipeline=%i, out_pipeline=%i, add_pipe=%i, prod_pipe=%i" % (i_d_w, 2 * i_d_w + 1, conj_b, inp_pipeline, out_pipeline, adder_pipeline, product_pipeline)
            obj.add_config(
                name = config_name,
                generics=dict(g_in_dat_w=i_d_w, g_out_dat_w=2*i_d_w + 1, g_conjugate_b=conj_b, g_pipeline_input=inp_pipeline, g_pipeline_product=product_pipeline, g_pipeline_adder=adder_pipeline,
                g_pipeline_output=out_pipeline, g_a_val_min=a_v_min, g_a_val_max=a_v_max, g_b_val_min=b_v_min, g_b_val_max=b_v_max)
            )

script_dir, _ = os.path.split(os.path.realpath(__file__))
# Create library 'casper_multiplier_lib'
lib1 = vu.add_library("casper_multiplier_lib", allow_duplicate=True)
txt = glob.glob(script_dir + "/*.vhd")
for x in txt:
    s = x.split('/')[-1]
    lib1.add_source_files(x)

inp_pipeline_values = 1 #+ random.sample([0,1], 1)
product_pipeline_values = 0 #+random.sample([0,1], 1)
adder_pipeline_values = 1 #+random.sample([0,1], 1)
out_pipeline_values = 1 #+ random.sample([0,1], 1)
in_dat_w_values = [18] + sample(range(4, 8), 1) 
conj_values = [True,False]

TB_GENERATED_1 = lib1.test_bench("tb_tb_vu_common_complex_mult")
TB_GENERATED_2 = lib1.test_bench("tb_tb_vu_common_mult")
# TB_GENERATED = lib1.test_bench("tb_common_complex_mult")

generate_tests(
    TB_GENERATED_1,
    in_dat_w_values,
    inp_pipeline_values,
    product_pipeline_values,
    out_pipeline_values,
    conj_values,
    adder_pipeline_values
)
generate_tests(
    TB_GENERATED_2,
    in_dat_w_values,
    inp_pipeline_values,
    product_pipeline_values,
    out_pipeline_values
)

# Create library 'common_components_lib'
lib2 = vu.add_library("common_components_lib",allow_duplicate=True)
lib2.add_source_files(script_dir + "/../common_components/common_pipeline.vhd")
lib2.add_source_files(script_dir + "/../common_components/common_pipeline_sl.vhd")

# Create library 'common_pkg_lib'
lib3 = vu.add_library("common_pkg_lib",allow_duplicate = True)
lib3.add_source_files(script_dir + "/../common_pkg/*.vhd")
lib3.add_source_files(script_dir + "/../common_pkg/tb_common_pkg.vhd")

lib4 = vu.add_library("technology_lib",allow_duplicate = True)
lib4.add_source_files(script_dir + "/../technology/technology_select_pkg.vhd")

lib5 = vu.add_library("ip_xpm_mult_lib", allow_duplicate=True)
lib5.add_source_files(script_dir + "/../ip_xpm/mult/*.vhd")

lib6 = vu.add_library("ip_stratixiv_mult_lib", allow_duplicate=True)
lib6.add_source_files(script_dir + "/../ip_stratixiv/mult/*rtl.vhd")
       
# Run vunit function
vu.set_compile_option("ghdl.a_flags", ["-frelaxed"])
vu.set_sim_option("ghdl.elab_flags", ["-frelaxed","--syn-binding"])
vu.main()
