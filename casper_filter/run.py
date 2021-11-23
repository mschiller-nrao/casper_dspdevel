from vunit import VUnit
from os.path import join, dirname

# Create VUnit instance by parsing command line arguments
vu = VUnit.from_argv()
script_dir = dirname(__file__)

# XPM Library compile
lib_xpm = vu.add_library("xpm")
lib_xpm.add_source_files(join(script_dir, "../xilinx/xpm_vhdl/src/xpm/xpm_VCOMP.vhd"))
xpm_source_file_base = lib_xpm.add_source_file(join(script_dir, "../xilinx/xpm_vhdl/src/xpm/xpm_memory/hdl/xpm_memory_base.vhd"))
xpm_source_file_sdpram = lib_xpm.add_source_file(join(script_dir, "../xilinx/xpm_vhdl/src/xpm/xpm_memory/hdl/xpm_memory_sdpram.vhd"))
xpm_source_file_tdpram = lib_xpm.add_source_file(join(script_dir, "../xilinx/xpm_vhdl/src/xpm/xpm_memory/hdl/xpm_memory_tdpram.vhd"))
xpm_source_file_sdpram.add_dependency_on(xpm_source_file_base)
xpm_source_file_tdpram.add_dependency_on(xpm_source_file_base)

# Altera_mf library
lib_altera_mf = vu.add_library("altera_mf")
lib_altera_mf.add_source_file(join(script_dir, "../intel/altera_mf/altera_mf_components.vhd"))
altera_mf_source_file = lib_altera_mf.add_source_file(join(script_dir, "../intel/altera_mf/altera_mf.vhd"))

# XPM Multiplier library
ip_xpm_mult_lib = vu.add_library("ip_xpm_mult_lib", allow_duplicate=True)
ip_mult_infer = ip_xpm_mult_lib.add_source_file(join(script_dir, "../ip_xpm/mult/ip_mult_infer.vhd"))

# STRATIXIV Multiplier library
ip_stratixiv_mult_lib = vu.add_library("ip_stratixiv_mult_lib", allow_duplicate=True)
ip_stratixiv_mult_rtl = ip_stratixiv_mult_lib.add_source_file(join(script_dir, "../ip_stratixiv/mult/ip_stratixiv_mult_rtl.vhd"))

# XPM RAM library
ip_xpm_ram_lib = vu.add_library("ip_xpm_ram_lib")
ip_xpm_file_cr_cw = ip_xpm_ram_lib.add_source_files(join(script_dir, "../ip_xpm/ram/ip_xpm_ram_cr_cw.vhd"))
ip_xpm_file_crw_crw = ip_xpm_ram_lib.add_source_files(join(script_dir, "../ip_xpm/ram/ip_xpm_ram_crw_crw.vhd"))
ip_xpm_file_cr_cw.add_dependency_on(xpm_source_file_sdpram)
ip_xpm_file_crw_crw.add_dependency_on(xpm_source_file_tdpram)

# STRATIXIV RAM Library
ip_stratixiv_ram_lib = vu.add_library("ip_stratixiv_ram_lib")
ip_stratix_file_cr_cw = ip_stratixiv_ram_lib.add_source_file(join(script_dir, "../ip_stratixiv/ram/ip_stratixiv_ram_cr_cw.vhd"))
ip_stratix_file_crw_crw = ip_stratixiv_ram_lib.add_source_file(join(script_dir, "../ip_stratixiv/ram/ip_stratixiv_ram_crw_crw.vhd"))
ip_stratix_file_cr_cw.add_dependency_on(altera_mf_source_file)
ip_stratix_file_crw_crw.add_dependency_on(altera_mf_source_file)

# COMMON COMPONENTS Library 
common_components_lib = vu.add_library("common_components_lib")
common_components_lib.add_source_files(join(script_dir, "../common_components/common_pipeline.vhd"))
common_components_lib.add_source_files(join(script_dir, "../common_components/common_pipeline_sl.vhd"))

# COMMON PACKAGE Library
common_pkg_lib = vu.add_library("common_pkg_lib")
common_pkg_lib.add_source_files(join(script_dir, "../common_pkg/common_pkg.vhd"))
common_pkg_lib.add_source_files(join(script_dir, "../common_pkg/tb_common_pkg.vhd"))
common_pkg_lib.add_source_files(join(script_dir, "../common_pkg/common_lfsr_sequences_pkg.vhd"))

# TECHNOLOGY Library
technology_lib = vu.add_library("technology_lib")
technology_lib.add_source_files(join(script_dir, "../technology/technology_select_pkg.vhd"))

# CASPER ADDER Library
casper_adder_lib = vu.add_library("casper_adder_lib")
casper_adder_lib.add_source_file(join(script_dir,"../casper_adder/common_add_sub.vhd"))
casper_adder_lib.add_source_file(join(script_dir,"../casper_adder/common_adder_tree_a_str.vhd"))
casper_adder_lib.add_source_file(join(script_dir,"../casper_adder/common_adder_tree.vhd"))

# CASPER MUlTIPLIER Library
casper_multiplier_lib = vu.add_library("casper_multiplier_lib")
casper_multiplier_lib.add_source_file(join(script_dir, "../casper_multiplier/tech_mult_component.vhd"))
tech_mult = casper_multiplier_lib.add_source_file(join(script_dir, "../casper_multiplier/tech_mult.vhd"))
casper_multiplier_lib.add_source_file(join(script_dir, "../casper_multiplier/common_mult.vhd"))
tech_mult.add_dependency_on(ip_mult_infer)

# CASPER REQUANTIZE Library
casper_requantize_lib = vu.add_library("casper_requantize_lib")
casper_requantize_lib.add_source_file(join(script_dir, "../casper_requantize/common_round.vhd"))
casper_requantize_lib.add_source_file(join(script_dir, "../casper_requantize/common_resize.vhd"))
casper_requantize_lib.add_source_file(join(script_dir, "../casper_requantize/common_requantize.vhd"))

# CASPER RAM Library
casper_ram_lib = vu.add_library("casper_ram_lib")
casper_ram_lib.add_source_file(join(script_dir, "../casper_ram/common_ram_pkg.vhd"))
casper_ram_lib.add_source_file(join(script_dir, "../casper_ram/tech_memory_component_pkg.vhd"))
casper_ram_lib.add_source_file(join(script_dir, "../casper_ram/tech_memory_ram_crw_crw.vhd"))
casper_ram_lib.add_source_file(join(script_dir, "../casper_ram/tech_memory_ram_cr_cw.vhd"))
casper_ram_lib.add_source_file(join(script_dir, "../casper_ram/common_ram_crw_crw.vhd"))
casper_ram_lib.add_source_file(join(script_dir, "../casper_ram/common_ram_rw_rw.vhd"))
casper_ram_lib.add_source_file(join(script_dir, "../casper_ram/common_ram_r_w.vhd"))

# CASPER FILTER Library
casper_filter_lib = vu.add_library("casper_filter_lib")
casper_filter_lib.add_source_file(join(script_dir,"./fil_pkg.vhd"))
casper_filter_lib.add_source_file(join(script_dir,"./fil_ppf_ctrl.vhd"))
casper_filter_lib.add_source_file(join(script_dir,"./fil_ppf_filter.vhd"))
casper_filter_lib.add_source_file(join(script_dir,"./fil_ppf_single.vhd"))
casper_filter_lib.add_source_file(join(script_dir,"./tb_fil_ppf_single.vhd"))
casper_filter_lib.add_source_file(join(script_dir,"./tb_tb_vu_fil_ppf_single.vhd"))
# casper_filter_lib.add_source_file(join(script_dir,"./fil_ppf_wide.vhd"))
# casper_filter_lib.add_source_file(join(script_dir,"./tb_fil_ppf_wide.vhd"))
# casper_filter_lib.add_source_file(join(script_dir,"./tb_tb_vu_fil_ppf_wide.vhd"))

#CONSTANTS FOR SINGLE FILTER

c_file_prefix_8 = join(script_dir, "./data/hex/run_pfir_coeff_m_incrementing_8taps_64points_16b")
c_file_prefix_9 = join(script_dir, "./data/hex/run_pfir_coeff_m_incrementing_9taps_64points_16b")

c_act = dict(
    g_wb_factor = 1,
    g_nof_chan = 0,
    g_nof_bands = 64,
    g_nof_taps = 8,
    g_nof_streams = 1,
    g_backoff_w = 0,
    g_fil_in_dat_w = 8,
    g_fil_out_dat_w = 16,
    g_coef_dat_w = 16,
    g_coefs_file_prefix = c_file_prefix_8,
    g_enable_in_val_gaps = False
)
c_rnd_quant = c_act.copy()
c_rnd_quant.update({'g_enable_in_val_gaps':True})
c_rnd_9taps = c_rnd_quant.copy()
c_rnd_9taps.update({'g_nof_taps':9,'g_coefs_file_prefix':c_file_prefix_9})
c_rnd_3streams =  c_rnd_9taps.copy()
c_rnd_3streams.update({'g_nof_streams':3})
c_rnd_4channels = c_rnd_3streams.copy()
c_rnd_4channels.update({'g_nof_chan':2})

TB_SINGLE_FILTER = casper_filter_lib.test_bench("tb_tb_vu_fil_ppf_single")
TB_SINGLE_FILTER.add_config(
    name = 'u_act',
    generics=c_act
)
TB_SINGLE_FILTER.add_config(
    name = 'u_rnd_quant',
    generics=c_rnd_quant
)
TB_SINGLE_FILTER.add_config(
    name = 'u_rnd_9taps',
    generics=c_rnd_9taps
)
TB_SINGLE_FILTER.add_config(
    name = 'u_rnd_3streams',
    generics=c_rnd_3streams
)
TB_SINGLE_FILTER.add_config(
    name = 'u_rnd_4channels',
    generics=c_rnd_4channels
)

# Run vunit function
vu.set_compile_option("ghdl.a_flags", ["-frelaxed","-fsynopsys","-fexplicit","-Wno-hide"])
vu.set_sim_option("ghdl.elab_flags", ["-frelaxed","-fsynopsys","-fexplicit","--syn-binding"])
vu.main()