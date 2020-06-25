
LIBRARY IEEE, common_pkg_lib;
USE IEEE.std_logic_1164.ALL;
USE common_pkg_lib.common_pkg.ALL;
USE work.tech_mult_component_pkg.all;

ENTITY tech_mult IS
	GENERIC(
		g_sim              : BOOLEAN := TRUE;
		g_sim_level        : NATURAL := 0; -- 0: Simulate variant passed via g_variant for given g_technology
		g_technology       : NATURAL := 0;
		g_use_dsp		   : STRING := "YES"; --! Implement multiplications in DSP48 or not
		g_in_a_w           : POSITIVE;
		g_in_b_w           : POSITIVE;
		g_out_p_w          : POSITIVE;  -- default use g_out_p_w = g_in_a_w+g_in_b_w = c_prod_w
		g_pipeline_input   : NATURAL := 1; -- 0 or 1
		g_pipeline_product : NATURAL := 0; -- 0 or 1
		g_pipeline_output  : NATURAL := 1 -- >= 0
	);
	PORT(
		rst       : IN  STD_LOGIC := '0';
		clk       : IN  STD_LOGIC;
		clken     : IN  STD_LOGIC := '1';
		in_a     : IN  STD_LOGIC_VECTOR(g_in_a_w - 1 DOWNTO 0);
		in_b     : IN  STD_LOGIC_VECTOR(g_in_b_w - 1 DOWNTO 0);
		result   : OUT STD_LOGIC_VECTOR(g_out_p_w - 1 DOWNTO 0)
	);
END tech_mult;

ARCHITECTURE str of tech_mult is
	
	CONSTANT c_dsp_dat_w  : NATURAL := 18;
	CONSTANT c_dsp_prod_w : NATURAL := 2 * c_dsp_dat_w;

	SIGNAL a      : STD_LOGIC_VECTOR(c_dsp_dat_w - 1 DOWNTO 0);
	SIGNAL b      : STD_LOGIC_VECTOR(c_dsp_dat_w - 1 DOWNTO 0);
	SIGNAL mult   : STD_LOGIC_VECTOR(c_dsp_prod_w - 1 DOWNTO 0);

	-- sim_model=1
	SIGNAL result_undelayed : STD_LOGIC_VECTOR(g_in_b_w + g_in_a_w - 1 DOWNTO 0);
	begin
	
	gen_xilinx_mult : ip_mult_infer
		generic map(
			g_use_dsp          => g_use_dsp,
			g_in_a_w           => g_in_a_w,
			g_in_b_w           => g_in_b_w,
			g_out_p_w          => g_out_p_w,
			g_pipeline_input   => g_pipeline_input,
			g_pipeline_product => g_pipeline_product,
			g_pipeline_output  => g_pipeline_output
		)
		port map(
			in_a  => in_a,
			in_b  => in_b,
			clk   => clk,
			rst   => rst,
			ce    => clken,
			out_p => result
		);
	
	end str;