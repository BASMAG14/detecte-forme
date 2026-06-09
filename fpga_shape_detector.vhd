-- FPGA Shape Detector Receiver
-- Ce module reçoit les signaux de détection de formes via UART
-- et contrôle des LEDs ou autres périphériques selon la forme détectée

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity shape_detector_fpga is
    Port (
        clk : in STD_LOGIC;                    -- Horloge système (ex: 50MHz)
        reset : in STD_LOGIC;                  -- Reset asynchrone

        -- Interface UART (RX seulement)
        rx : in STD_LOGIC;                     -- Réception UART

        -- Sorties de contrôle
        led_cube : out STD_LOGIC;              -- LED pour cube (forme 1)
        led_cylinder : out STD_LOGIC;          -- LED pour cylindre (forme 2)
        led_triangle : out STD_LOGIC;          -- LED pour triangle (forme 3)
        led_unknown : out STD_LOGIC;           -- LED pour forme inconnue (forme 0)

        -- Sortie pour débogage
        shape_code : out STD_LOGIC_VECTOR(1 downto 0)  -- Code de la forme actuelle
    );
end shape_detector_fpga;

architecture Behavioral of shape_detector_fpga is

    -- États de la machine à états
    type state_type is (IDLE, RECEIVE_DATA, PROCESS_DATA);
    signal state : state_type := IDLE;

    -- Signaux UART
    signal uart_data : STD_LOGIC_VECTOR(7 downto 0);
    signal uart_data_valid : STD_LOGIC := '0';

    -- Registre pour stocker la forme actuelle
    signal current_shape : STD_LOGIC_VECTOR(1 downto 0) := "00";

    -- Composant UART Receiver (vous devrez l'implémenter ou utiliser une IP)
    component uart_rx
        generic (
            BAUD_RATE : integer := 9600;
            CLK_FREQ : integer := 50000000
        );
        port (
            clk : in STD_LOGIC;
            reset : in STD_LOGIC;
            rx : in STD_LOGIC;
            data_out : out STD_LOGIC_VECTOR(7 downto 0);
            data_valid : out STD_LOGIC
        );
    end component;

begin

    -- Instance du récepteur UART
    uart_receiver : uart_rx
        generic map (
            BAUD_RATE => 9600,
            CLK_FREQ => 50000000
        )
        port map (
            clk => clk,
            reset => reset,
            rx => rx,
            data_out => uart_data,
            data_valid => uart_data_valid
        );

    -- Machine à états principale
    process(clk, reset)
    begin
        if reset = '1' then
            state <= IDLE;
            current_shape <= "00";
        elsif rising_edge(clk) then
            case state is
                when IDLE =>
                    if uart_data_valid = '1' then
                        state <= RECEIVE_DATA;
                    end if;

                when RECEIVE_DATA =>
                    -- Traiter les données reçues
                    case uart_data is
                        when "00110001" =>  -- Caractère '1' (ASCII 49)
                            current_shape <= "01";  -- Cube
                        when "00110010" =>  -- Caractère '2' (ASCII 50)
                            current_shape <= "10";  -- Cylindre
                        when "00110011" =>  -- Caractère '3' (ASCII 51)
                            current_shape <= "11";  -- Triangle
                        when others =>
                            current_shape <= "00";  -- Inconnu
                    end case;
                    state <= PROCESS_DATA;

                when PROCESS_DATA =>
                    -- Attendre un peu puis revenir à IDLE
                    state <= IDLE;

                when others =>
                    state <= IDLE;
            end case;
        end if;
    end process;

    -- Décodage des sorties LED
    led_cube <= '1' when current_shape = "01" else '0';
    led_cylinder <= '1' when current_shape = "10" else '0';
    led_triangle <= '1' when current_shape = "11" else '0';
    led_unknown <= '1' when current_shape = "00" else '0';

    -- Sortie du code de forme pour débogage
    shape_code <= current_shape;

end Behavioral;