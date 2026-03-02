"""
ElectroNoob-less: Independent Power Architect
==============================================
An Expert System for Designing Off-Grid Renewable Energy Systems
Based on Pure Physics Laws: Faraday, Ohm, Joule, and Betz

Author: AI Assistant
Version: 1.0.0
"""

import streamlit as st
import math
import numpy as np
from dataclasses import dataclass
from typing import Dict, Tuple, Optional
from enum import Enum

# =============================================================================
# PAGE CONFIGURATION (MUST BE FIRST STREAMLIT COMMAND)
# =============================================================================
st.set_page_config(
    page_title="ElectroNoob-less: Power Architect",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS FOR MOBILE-FIRST RESPONSIVE DESIGN
# =============================================================================
st.markdown("""
<style>
    /* Mobile-first responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        .stMetric {
            font-size: 0.9rem;
        }
    }
    
    /* Traffic light indicators */
    .traffic-green {
        background: linear-gradient(135deg, #00b894, #00a085);
        color: white;
        padding: 10px 15px;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,184,148,0.3);
    }
    .traffic-yellow {
        background: linear-gradient(135deg, #fdcb6e, #f39c12);
        color: #2d3436;
        padding: 10px 15px;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 2px 8px rgba(253,203,110,0.3);
    }
    .traffic-red {
        background: linear-gradient(135deg, #e17055, #d63031);
        color: white;
        padding: 10px 15px;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 2px 8px rgba(225,112,85,0.3);
    }
    
    /* Physics insight cards */
    .physics-card {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(116,185,255,0.3);
    }
    .physics-title {
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .physics-formula {
        background: rgba(255,255,255,0.2);
        padding: 8px 12px;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
        margin: 8px 0;
    }
    
    /* Reality check badge */
    .reality-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .reality-possible {
        background: #00b894;
        color: white;
    }
    .reality-challenging {
        background: #fdcb6e;
        color: #2d3436;
    }
    .reality-impossible {
        background: #e17055;
        color: white;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #6c5ce7, #a29bfe);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        margin: 20px 0 15px 0;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    /* Result cards */
    .result-card {
        background: #f8f9fa;
        border-left: 4px solid #6c5ce7;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# CONSTANTS & PHYSICAL PARAMETERS
# =============================================================================

class BatteryType(Enum):
    LEAD_ACID = "Lead Acid (VRLA/AGM)"
    LIFEPO4 = "LiFePO4 (Lithium)"

class VoltageTarget(Enum):
    V5 = 5
    V12 = 12
    V24 = 24
    V48 = 48
    V220 = 220

# Physical Constants
RHO_AIR = 1.225  # kg/m³, air density at sea level
BETZ_LIMIT = 16/27  # 0.593, maximum theoretical efficiency
CP_PRACTICAL = 0.35  # 35% practical turbine efficiency
MAGNET_N52_BR = 1.48  # Tesla, remanence of N52 magnet
MU_0 = 4 * math.pi * 1e-7  # H/m, permeability of free space
RHO_COPPER = 1.68e-8  # Ω·m, copper resistivity
ALUMINUM_RHO = 2.65e-8  # Ω·m, aluminum resistivity

# Battery parameters
BATTERY_PARAMS = {
    BatteryType.LEAD_ACID: {
        "dod_max": 0.50,  # 50% depth of discharge
        "efficiency": 0.85,
        "cycles": 500,
        "temp_coeff": -0.005  # per °C
    },
    BatteryType.LIFEPO4: {
        "dod_max": 0.90,  # 90% depth of discharge
        "efficiency": 0.95,
        "cycles": 3000,
        "temp_coeff": -0.001
    }
}

# Wire gauge properties (AWG to mm conversion and current capacity)
WIRE_SPECS = {
    0.5: {"max_amps": 3, "ohms_per_km": 89.4},
    0.75: {"max_amps": 5, "ohms_per_km": 59.6},
    1.0: {"max_amps": 8, "ohms_per_km": 44.6},
    1.5: {"max_amps": 12, "ohms_per_km": 29.7},
    2.5: {"max_amps": 18, "ohms_per_km": 17.8},
    4.0: {"max_amps": 25, "ohms_per_km": 11.1},
    6.0: {"max_amps": 35, "ohms_per_km": 7.4},
    10.0: {"max_amps": 50, "ohms_per_km": 4.5},
    16.0: {"max_amps": 70, "ohms_per_km": 2.8},
}

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class WindParameters:
    wind_speed: float  # m/s
    turbine_diameter: float  # meters
    air_density: float = RHO_AIR

@dataclass
class LoadParameters:
    total_watts: float
    usage_hours: float
    cable_distance: float
    autonomy_days: int
    target_voltage: VoltageTarget
    battery_type: BatteryType
    wire_diameter: float

@dataclass
class TransmissionParameters:
    pulley_driver: float  # mm, turbine side
    pulley_driven: float  # mm, generator side
    efficiency: float = 0.95

@dataclass
class SolarParameters:
    sun_hours: float
    panel_efficiency: float = 0.18
    charge_efficiency: float = 0.85

# =============================================================================
# WIND & AFG CALCULATION MODULE
# =============================================================================

class WindAFGModule:
    """
    Wind Turbine and Axial Flux Generator (AFG) Design Module
    Implements Betz Limit, torque calculations, and trapezoidal coil design
    """
    
    @staticmethod
    def calculate_betz_power(wind_params: WindParameters) -> Dict[str, float]:
        """
        Calculate theoretical and practical power from wind using Betz Limit
        P = 0.5 * ρ * A * v³ * Cp
        """
        area = math.pi * (wind_params.turbine_diameter / 2) ** 2
        v = wind_params.wind_speed
        
        # Theoretical maximum (Betz Limit)
        power_theoretical = 0.5 * wind_params.air_density * area * v**3 * BETZ_LIMIT
        
        # Practical power (realistic Cp)
        power_practical = 0.5 * wind_params.air_density * area * v**3 * CP_PRACTICAL
        
        # Cut-in and cut-out speeds
        cut_in_speed = 3.0  # m/s typical
        cut_out_speed = 25.0  # m/s typical
        
        if v < cut_in_speed:
            status = "insufficient"
            power_practical = 0
        elif v > cut_out_speed:
            status = "excessive"
            power_practical = 0
        else:
            status = "optimal"
        
        return {
            "power_theoretical_w": power_theoretical,
            "power_practical_w": power_practical,
            "swept_area_m2": area,
            "cut_in_speed": cut_in_speed,
            "cut_out_speed": cut_out_speed,
            "status": status,
            "cp_theoretical": BETZ_LIMIT,
            "cp_practical": CP_PRACTICAL
        }
    
    @staticmethod
    def calculate_turbine_torque(power_w: float, rpm: float) -> Dict[str, float]:
        """
        Calculate torque from power and RPM
        T = P / ω = P / (2π * RPM / 60)
        """
        if rpm == 0:
            return {"torque_nm": 0, "omega_rad_s": 0}
        
        omega = 2 * math.pi * rpm / 60  # rad/s
        torque = power_w / omega  # Nm
        
        return {
            "torque_nm": torque,
            "omega_rad_s": omega,
            "rpm": rpm
        }
    
    @staticmethod
    def calculate_reducer_ratio(transmission: TransmissionParameters) -> Dict[str, float]:
        """
        Calculate gear/pulley reducer ratio
        Ratio = D_driven / D_driver
        """
        ratio = transmission.pulley_driven / transmission.pulley_driver
        rpm_output = 100 * ratio  # Assuming 100 RPM input for estimation
        
        return {
            "ratio": ratio,
            "rpm_output": rpm_output,
            "torque_multiplier": ratio * transmission.efficiency,
            "efficiency": transmission.efficiency
        }
    
    @staticmethod
    def design_afg_generator(target_voltage: float, rpm: float, 
                              magnet_grade: str = "N52") -> Dict[str, any]:
        """
        Design Axial Flux Generator with trapezoidal coils
        Uses Faraday's Law: EMF = N * dΦ/dt
        
        For N52 magnets: Br = 1.48 T
        """
        magnet_br = MAGNET_N52_BR
        
        # Estimate flux per pole (simplified)
        # Assuming 20mm x 20mm x 10mm N52 magnets
        magnet_area = 0.020 * 0.020  # m²
        flux_per_pole = magnet_br * magnet_area  # Weber
        
        # Frequency at given RPM (assuming 12 poles = 6 pole pairs)
        pole_pairs = 6
        frequency = (rpm * pole_pairs) / 60  # Hz
        
        # Required turns calculation using Faraday's Law
        # V = 4.44 * f * N * Φ * k_w (winding factor ~0.9)
        winding_factor = 0.9
        if frequency > 0:
            required_turns = target_voltage / (4.44 * frequency * flux_per_pole * winding_factor)
        else:
            required_turns = float('inf')
        
        # Trapezoidal coil geometry
        # Inner radius, outer radius, coil width
        inner_radius = 0.060  # 60mm
        outer_radius = 0.120  # 120mm
        coil_width = outer_radius - inner_radius
        
        # Mean turn length
        mean_radius = (inner_radius + outer_radius) / 2
        mean_turn_length = 2 * math.pi * mean_radius
        
        # Wire length estimation
        wire_length = required_turns * mean_turn_length
        
        # Coil resistance (using 0.8mm wire as default)
        wire_diameter = 0.8e-3  # meters
        wire_area = math.pi * (wire_diameter / 2) ** 2
        resistance = RHO_COPPER * wire_length / wire_area
        
        # Current capacity (conservative)
        max_current = 5  # A for 0.8mm wire
        
        return {
            "magnet_type": magnet_grade,
            "magnet_br": magnet_br,
            "flux_per_pole_wb": flux_per_pole,
            "pole_pairs": pole_pairs,
            "frequency_hz": frequency,
            "required_turns": int(required_turns),
            "coil_geometry": {
                "inner_radius_mm": inner_radius * 1000,
                "outer_radius_mm": outer_radius * 1000,
                "width_mm": coil_width * 1000
            },
            "wire_length_m": wire_length,
            "coil_resistance_ohm": resistance,
            "max_current_a": max_current,
            "max_power_w": target_voltage * max_current,
            "voltage_constant": target_voltage / rpm if rpm > 0 else 0  # V/RPM
        }
    
    @staticmethod
    def calculate_wire_heating(current: float, wire_diameter: float, 
                               ambient_temp: float = 30) -> Dict[str, any]:
        """
        Calculate wire heating using Joule's Law: P = I²R
        Estimate temperature rise
        """
        # Wire resistance per meter
        area = math.pi * (wire_diameter / 2) ** 2
        resistance_per_m = RHO_COPPER / area
        
        # Power dissipation per meter
        power_dissipation = current ** 2 * resistance_per_m  # W/m
        
        # Temperature rise estimation (simplified)
        # ΔT = P / (h * A) where h is heat transfer coefficient
        # For natural convection: h ≈ 10-25 W/m²K
        h_natural = 15  # W/m²K
        surface_area_per_m = math.pi * wire_diameter  # m²/m
        
        temp_rise = power_dissipation / (h_natural * surface_area_per_m)
        final_temp = ambient_temp + temp_rise
        
        # PVC insulation limit
        pvc_limit = 70  # °C
        
        if final_temp < pvc_limit * 0.6:
            status = "safe"
            color = "green"
        elif final_temp < pvc_limit * 0.85:
            status = "warm"
            color = "yellow"
        else:
            status = "critical"
            color = "red"
        
        return {
            "resistance_per_m": resistance_per_m,
            "power_dissipation_w_per_m": power_dissipation,
            "temperature_rise_c": temp_rise,
            "final_temperature_c": final_temp,
            "pvc_limit_c": pvc_limit,
            "status": status,
            "color": color,
            "current_density_a_mm2": current / (area * 1e6)  # A/mm²
        }

# =============================================================================
# SOLAR & BATTERY MODULE
# =============================================================================

class SolarBatteryModule:
    """
    Solar Panel and Battery Sizing Module
    Implements battery capacity calculations with DoD limits
    """
    
    @staticmethod
    def calculate_battery_capacity(load: LoadParameters) -> Dict[str, any]:
        """
        Calculate required battery capacity considering:
        - Daily energy consumption
        - Autonomy days
        - Depth of Discharge (DoD) limit
        - System voltage
        """
        daily_energy_wh = load.total_watts * load.usage_hours
        total_energy_needed = daily_energy_wh * load.autonomy_days
        
        # Get battery parameters
        battery_params = BATTERY_PARAMS[load.battery_type]
        dod_limit = battery_params["dod_max"]
        efficiency = battery_params["efficiency"]
        
        # Account for efficiency losses
        adjusted_energy = total_energy_needed / efficiency
        
        # Apply DoD limit - need more capacity to deliver same energy
        required_wh = adjusted_energy / dod_limit
        
        # Convert to Ah at system voltage
        voltage = load.target_voltage.value
        required_ah = required_wh / voltage
        
        # Round up to practical values
        practical_ah = math.ceil(required_ah / 10) * 10
        
        # Series/parallel configuration
        if voltage == 12:
            cells_series = 4 if load.battery_type == BatteryType.LIFEPO4 else 6
        elif voltage == 24:
            cells_series = 8 if load.battery_type == BatteryType.LIFEPO4 else 12
        elif voltage == 48:
            cells_series = 16 if load.battery_type == BatteryType.LIFEPO4 else 24
        else:
            cells_series = 1
        
        return {
            "daily_energy_wh": daily_energy_wh,
            "total_energy_needed_wh": total_energy_needed,
            "adjusted_energy_wh": adjusted_energy,
            "required_capacity_wh": required_wh,
            "required_capacity_ah": required_ah,
            "practical_capacity_ah": practical_ah,
            "system_voltage_v": voltage,
            "dod_limit_percent": dod_limit * 100,
            "usable_energy_wh": practical_ah * voltage * dod_limit,
            "cells_series": cells_series,
            "battery_type": load.battery_type.value,
            "efficiency": efficiency,
            "autonomy_days": load.autonomy_days
        }
    
    @staticmethod
    def recommend_solar_panel(battery_capacity_ah: float, system_voltage: float,
                              solar: SolarParameters, autonomy_days: int) -> Dict[str, any]:
        """
        Recommend solar panel Watt-Peak to recharge battery in 2 sunny days
        """
        battery_wh = battery_capacity_ah * system_voltage
        
        # Energy to replenish (accounting for DoD)
        energy_to_replenish = battery_wh * 0.5  # Assuming 50% discharge
        
        # Target: recharge in 2 sunny days
        target_days = 2
        required_daily_energy = energy_to_replenish / target_days
        
        # Account for charge efficiency
        required_panel_output = required_daily_energy / solar.charge_efficiency
        
        # Calculate required WP
        if solar.sun_hours > 0:
            required_wp = required_panel_output / solar.sun_hours
        else:
            required_wp = float('inf')
        
        # Practical recommendation (round up)
        practical_wp = math.ceil(required_wp / 50) * 50
        
        # Panel configuration
        standard_panel_wp = 100  # Common 100W panel
        num_panels = math.ceil(practical_wp / standard_panel_wp)
        
        # Actual recharge time
        actual_recharge_days = energy_to_replenish / (practical_wp * solar.sun_hours * solar.charge_efficiency)
        
        return {
            "battery_capacity_wh": battery_wh,
            "energy_to_replenish_wh": energy_to_replenish,
            "required_daily_wh": required_daily_energy,
            "required_wp": required_wp,
            "recommended_wp": practical_wp,
            "standard_panel_wp": standard_panel_wp,
            "num_panels": num_panels,
            "estimated_recharge_days": actual_recharge_days,
            "sun_hours": solar.sun_hours,
            "charge_efficiency": solar.charge_efficiency
        }

# =============================================================================
# SYSTEM ADVISOR MODULE
# =============================================================================

class SystemAdvisor:
    """
    System-level analysis and recommendations
    Includes inverter losses, voltage drop calculations, and optimization advice
    """
    
    @staticmethod
    def calculate_inverter_loss(dc_power: float, inverter_efficiency: float = 0.85) -> Dict[str, float]:
        """
        Calculate inverter conversion losses
        """
        ac_power = dc_power * inverter_efficiency
        loss = dc_power - ac_power
        
        return {
            "dc_power_w": dc_power,
            "ac_power_w": ac_power,
            "loss_w": loss,
            "efficiency": inverter_efficiency,
            "loss_percent": (1 - inverter_efficiency) * 100
        }
    
    @staticmethod
    def calculate_voltage_drop(current: float, distance: float, 
                               wire_diameter: float, voltage: float) -> Dict[str, any]:
        """
        Calculate voltage drop using Ohm's Law: V_drop = I * R
        R = ρ * L / A (for round trip, L = 2 * distance)
        """
        # Round trip distance
        total_length = 2 * distance
        
        # Wire resistance
        area = math.pi * (wire_diameter / 2) ** 2
        resistance = RHO_COPPER * total_length / area
        
        # Voltage drop
        v_drop = current * resistance
        v_drop_percent = (v_drop / voltage) * 100
        
        # Status evaluation
        if v_drop_percent < 3:
            status = "excellent"
            color = "green"
            recommendation = "Kabel sesuai, tidak perlu perubahan"
        elif v_drop_percent < 5:
            status = "good"
            color = "green"
            recommendation = "Dalam batas aman (<5%)"
        elif v_drop_percent < 10:
            status = "marginal"
            color = "yellow"
            recommendation = "Pertimbangkan kabel lebih besar atau naikkan tegangan sistem"
        else:
            status = "critical"
            color = "red"
            recommendation = "WAJIB naikkan tegangan sistem atau gunakan kabel lebih besar!"
        
        return {
            "current_a": current,
            "distance_m": distance,
            "wire_diameter_mm": wire_diameter,
            "resistance_ohm": resistance,
            "voltage_drop_v": v_drop,
            "voltage_drop_percent": v_drop_percent,
            "remaining_voltage_v": voltage - v_drop,
            "status": status,
            "color": color,
            "recommendation": recommendation
        }
    
    @staticmethod
    def recommend_voltage_upgrade(current_voltage: VoltageTarget, 
                                  v_drop_percent: float) -> Optional[VoltageTarget]:
        """
        Recommend voltage upgrade if drop > 10%
        """
        if v_drop_percent < 10:
            return None
        
        voltage_map = {
            VoltageTarget.V5: VoltageTarget.V12,
            VoltageTarget.V12: VoltageTarget.V24,
            VoltageTarget.V24: VoltageTarget.V48,
            VoltageTarget.V48: VoltageTarget.V220,
            VoltageTarget.V220: None  # Already highest
        }
        
        return voltage_map.get(current_voltage)
    
    @staticmethod
    def system_compatibility_check(wind_power: float, solar_power: float, 
                                   load_watts: float) -> Dict[str, any]:
        """
        Check if generated power can meet load requirements
        """
        total_generation = wind_power + solar_power
        
        if total_generation >= load_watts * 1.2:
            status = "surplus"
            color = "green"
            message = "Sistem menghasilkan surplus energi (20%+ margin)"
        elif total_generation >= load_watts:
            status = "balanced"
            color = "green"
            message = "Sistem seimbang, memenuhi kebutuhan beban"
        elif total_generation >= load_watts * 0.7:
            status = "deficit"
            color = "yellow"
            message = "Defisit energi, pertimbangkan kurangi beban atau tambah panel"
        else:
            status = "critical"
            color = "red"
            message = "Defisit kritis! Sistem tidak mampu memenuhi kebutuhan"
        
        return {
            "wind_power_w": wind_power,
            "solar_power_w": solar_power,
            "total_generation_w": total_generation,
            "load_watts": load_watts,
            "margin_percent": ((total_generation - load_watts) / load_watts) * 100,
            "status": status,
            "color": color,
            "message": message
        }

# =============================================================================
# PHYSICS EDUCATION MODULE
# =============================================================================

class PhysicsEducation:
    """
    Educational content about the physics laws used in calculations
    """
    
    @staticmethod
    def faraday_law() -> Dict[str, str]:
        return {
            "title": "⚡ Hukum Faraday: Induksi Elektromagnetik",
            "description": "Hukum Faraday menjelaskan bagaimana tegangan (EMF) diinduksi dalam kumparan ketika fluks magnet berubah.",
            "formula": "ε = -N × dΦ/dt",
            "variables": "ε = tegangan induksi (V), N = jumlah lilitan, dΦ/dt = perubahan fluks magnet (Wb/s)",
            "application": "Dalam generator AFG, magnet berputar mengubah fluks melalui koil, menghasilkan tegangan AC.",
            "insight": "Semakin banyak lilitan atau semakin cepat perubahan fluks, semakin tinggi tegangannya."
        }
    
    @staticmethod
    def ohm_law() -> Dict[str, str]:
        return {
            "title": "⚡ Hukum Ohm: Hubungan V, I, dan R",
            "description": "Hukum Ohm mendefinisikan hubungan antara tegangan, arus, dan hambatan dalam konduktor.",
            "formula": "V = I × R    atau    R = ρ × L / A",
            "variables": "V = tegangan (V), I = arus (A), R = hambatan (Ω), ρ = resistivitas, L = panjang, A = luas penampang",
            "application": "Menghitung voltage drop pada kabel: V_drop = I × R_kabel",
            "insight": "Kabel panjang dan tipis memiliki hambatan besar, menyebabkan kehilangan energi sebagai panas."
        }
    
    @staticmethod
    def joule_law() -> Dict[str, str]:
        return {
            "title": "⚡ Hukum Joule: Panas dari Arus",
            "description": "Hukum Joule menjelaskan bahwa energi listrik diubah menjadi panas ketika arus mengalir melalui hambatan.",
            "formula": "P = I² × R    atau    Q = I² × R × t",
            "variables": "P = daya panas (W), I = arus (A), R = hambatan (Ω), Q = energi panas (J), t = waktu (s)",
            "application": "Menghitung pemanasan kabel: Semakin besar arus, semakin panas kabel (kuadratik!).",
            "insight": "Menggandakan arus → empat kali lipat panas! Ini mengapa kabel untuk 220V lebih tipis dari 12V untuk daya sama."
        }
    
    @staticmethod
    def betz_limit() -> Dict[str, str]:
        return {
            "title": "⚡ Limit Betz: Efisiensi Turbin Maksimum",
            "description": "Limit Betz adalah batas teoritis efisiensi turbin angin: maksimum 59.3% energi kinetik angin bisa diubah jadi mekanik.",
            "formula": "Cp_max = 16/27 ≈ 0.593",
            "variables": "Cp = koefisien daya, ρ = densitas udara, A = area sapuan, v = kecepatan angin",
            "application": "Turbin nyata mencapai Cp = 0.30-0.45. Desain di atas 0.50 mustahil secara fisika!",
            "insight": "Energi angin ∝ v³. Kecepatan angin 2× = energi 8×! Lokasi dengan angin konsisten lebih penting dari turbin besar."
        }

# =============================================================================
# REALITY CHECK MODULE
# =============================================================================

class RealityCheck:
    """
    Physical reality verification - can this design actually be built?
    """
    
    @staticmethod
    def check_feasibility(wind_result: Dict, battery_result: Dict, 
                         vdrop_result: Dict, compatibility: Dict) -> Dict[str, any]:
        """
        Perform comprehensive feasibility check
        """
        issues = []
        warnings = []
        
        # Wind turbine checks
        if wind_result.get("status") == "insufficient":
            issues.append("Kecepatan angin di bawah cut-in (3 m/s minimum)")
        elif wind_result.get("status") == "excessive":
            issues.append("Kecepatan angin berbahaya (>25 m/s), perlu brake system")
        
        if wind_result.get("power_practical_w", 0) < 10:
            warnings.append("Daya angin sangat kecil, pertimbangkan solar utama")
        
        # Battery checks
        if battery_result.get("required_capacity_ah", 0) > 1000:
            issues.append("Kapasitas baterai terlalu besar untuk sistem DIY")
        
        if battery_result.get("autonomy_days", 1) > 3:
            warnings.append("Autonomi >3 hari memerlukan investasi baterai besar")
        
        # Voltage drop checks
        if vdrop_result.get("status") == "critical":
            issues.append("Voltage drop kritis (>10%), sistem tidak akan berfungsi")
        elif vdrop_result.get("status") == "marginal":
            warnings.append("Voltage drop tinggi, efisiensi menurun")
        
        # System balance
        if compatibility.get("status") == "critical":
            issues.append("Defisit daya kritis, beban melebihi kapasitas generasi")
        elif compatibility.get("status") == "deficit":
            warnings.append("Defisit daya, perlu modifikasi beban atau tambah panel")
        
        # Determine overall status
        if issues:
            overall_status = "IMPOSSIBLE"
            color = "red"
            message = "Desain ini TIDAK DAPAT dibangun. Perbaiki masalah kritis."
        elif warnings:
            overall_status = "CHALLENGING"
            color = "yellow"
            message = "Desain MUNGKIN tapi menantang. Pertimbangkan peringatan."
        else:
            overall_status = "POSSIBLE"
            color = "green"
            message = "Desain ini DAPAT dibangun secara fisik!"
        
        return {
            "status": overall_status,
            "color": color,
            "message": message,
            "issues": issues,
            "warnings": warnings,
            "recommendations": RealityCheck._generate_recommendations(issues, warnings)
        }
    
    @staticmethod
    def _generate_recommendations(issues: list, warnings: list) -> list:
        """Generate practical recommendations based on issues"""
        recommendations = []
        
        if any("angin" in i.lower() for i in issues):
            recommendations.append("Pertimbangkan lokasi dengan angin lebih kencang atau gunakan solar sebagai utama")
        
        if any("voltage drop" in i.lower() for i in issues + warnings):
            recommendations.append("Naikkan tegangan sistem (12V→24V→48V) atau gunakan kabel lebih tebal")
        
        if any("baterai" in i.lower() for i in issues):
            recommendations.append("Kurangi hari autonomi atau gunakan bateri LiFePO4 (DoD 90%)")
        
        if any("defisit" in i.lower() for i in issues + warnings):
            recommendations.append("Kurangi beban listrik atau tambah kapasitas panel surya")
        
        if not recommendations:
            recommendations.append("Sistem siap dibangun! Dokumentasikan dan mulai dengan prototipe kecil.")
        
        return recommendations

# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_traffic_light(status: str, message: str):
    """Render traffic light indicator"""
    if status == "green" or status in ["safe", "optimal", "excellent", "good", "balanced", "surplus", "POSSIBLE"]:
        st.markdown(f'<div class="traffic-green">✅ {message}</div>', unsafe_allow_html=True)
    elif status == "yellow" or status in ["warm", "marginal", "deficit", "CHALLENGING"]:
        st.markdown(f'<div class="traffic-yellow">⚠️ {message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="traffic-red">🚨 {message}</div>', unsafe_allow_html=True)

def render_physics_card(law_func):
    """Render physics education card"""
    law = law_func()
    with st.expander(f"📚 {law['title']}"):
        st.markdown(f"**{law['description']}**")
        st.markdown(f'<div class="physics-formula">{law["formula"]}</div>', unsafe_allow_html=True)
        st.markdown(f"📝 *Variabel:* {law['variables']}")
        st.markdown(f"🔧 *Aplikasi:* {law['application']}")
        st.info(f"💡 *Insight:* {law['insight']}")

def render_reality_badge(check: Dict):
    """Render reality check badge"""
    color_class = f"reality-{check['color']}" if check['color'] in ['green', 'yellow', 'red'] else "reality-challenging"
    st.markdown(f"""
    <div style="text-align: center; margin: 20px 0;">
        <span class="reality-badge {color_class}">
            {check['status']}: {check['message']}
        </span>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    # Header
    st.title("⚡ ElectroNoob-less: Independent Power Architect")
    st.markdown("*Sistem Pakar untuk Desain Energi Mandiri (Angin & Surya)*")
    st.markdown("---")
    
    # Sidebar - Input Parameters
    with st.sidebar:
        st.header("🔧 Parameter Input")
        
        # Natural Conditions
        st.subheader("🌬️ Kondisi Alam")
        wind_speed = st.slider(
            "Kecepatan Angin (m/s)",
            min_value=0.0,
            max_value=30.0,
            value=5.0,
            step=0.5,
            help="Kecepatan angin rata-rata di lokasi. Minimum 3 m/s untuk turbin bekerja."
        )
        
        sun_hours = st.slider(
            "Jam Matahari Efektif (jam/hari)",
            min_value=0.0,
            max_value=12.0,
            value=5.0,
            step=0.5,
            help="Jam sinar matahari puncak (1000 W/m²) per hari. Indonesia: 4-6 jam."
        )
        
        # Load Requirements
        st.subheader("⚡ Kebutuhan Beban")
        total_watts = st.number_input(
            "Total Watt Beban (W)",
            min_value=1,
            max_value=10000,
            value=100,
            step=10,
            help="Total daya semua perangkat yang akan dinyalakan."
        )
        
        usage_hours = st.slider(
            "Durasi Pakai (jam/hari)",
            min_value=0.5,
            max_value=24.0,
            value=8.0,
            step=0.5
        )
        
        cable_distance = st.slider(
            "Jarak Kabel (m)",
            min_value=1,
            max_value=100,
            value=10,
            step=1,
            help="Jarak dari panel/baterai ke beban. Affects voltage drop!"
        )
        
        autonomy_days = st.slider(
            "Hari Otonom (tanpa sinar/angin)",
            min_value=1,
            max_value=5,
            value=2,
            step=1,
            help="Berapa hari sistem bertahan tanpa generasi energi."
        )
        
        # Technical Specs
        st.subheader("🔩 Spesifikasi Teknis")
        
        voltage_options = {
            "5V (USB/Arduino)": VoltageTarget.V5,
            "12V (DC umum)": VoltageTarget.V12,
            "24V (DC industri)": VoltageTarget.V24,
            "48V (DC tinggi)": VoltageTarget.V48,
            "220V AC (PLN)": VoltageTarget.V220
        }
        target_voltage_str = st.selectbox(
            "Target Tegangan Sistem",
            options=list(voltage_options.keys()),
            index=1
        )
        target_voltage = voltage_options[target_voltage_str]
        
        battery_type = st.selectbox(
            "Jenis Baterai",
            options=[BatteryType.LEAD_ACID, BatteryType.LIFEPO4],
            format_func=lambda x: x.value
        )
        
        wire_diameter = st.selectbox(
            "Diameter Kawat (mm)",
            options=[0.5, 0.75, 1.0, 1.5, 2.5, 4.0, 6.0, 10.0, 16.0],
            index=4,
            help="Diameter penghantar kabel utama. Lebih besar = lebih sedikit panas."
        )
        
        # Transmission
        st.subheader("⚙️ Transmisi Mekanik")
        pulley_driver = st.slider(
            "Diameter Pulley Driver - Turbin (mm)",
            min_value=50,
            max_value=500,
            value=200,
            step=10
        )
        
        pulley_driven = st.slider(
            "Diameter Pulley Driven - Generator (mm)",
            min_value=50,
            max_value=500,
            value=100,
            step=10
        )
        
        turbine_diameter = st.slider(
            "Diameter Turbin Angin (m)",
            min_value=0.5,
            max_value=5.0,
            value=1.2,
            step=0.1
        )
    
    # Create parameter objects
    wind_params = WindParameters(
        wind_speed=wind_speed,
        turbine_diameter=turbine_diameter
    )
    
    load_params = LoadParameters(
        total_watts=total_watts,
        usage_hours=usage_hours,
        cable_distance=cable_distance,
        autonomy_days=autonomy_days,
        target_voltage=target_voltage,
        battery_type=battery_type,
        wire_diameter=wire_diameter
    )
    
    transmission = TransmissionParameters(
        pulley_driver=pulley_driver,
        pulley_driven=pulley_driven
    )
    
    solar_params = SolarParameters(
        sun_hours=sun_hours
    )
    
    # Calculate current for wire and voltage drop calculations
    current = total_watts / target_voltage.value
    
    # =================================================================
    # CALCULATIONS
    # =================================================================
    
    # Wind & AFG Module
    wind_module = WindAFGModule()
    wind_result = wind_module.calculate_betz_power(wind_params)
    reducer_result = wind_module.calculate_reducer_ratio(transmission)
    
    # Estimate turbine RPM (simplified: tip speed ratio ~6)
    tsr = 6
    tip_speed = wind_speed * tsr
    turbine_rpm = (tip_speed * 60) / (math.pi * turbine_diameter)
    generator_rpm = turbine_rpm * reducer_result["ratio"]
    
    torque_result = wind_module.calculate_turbine_torque(wind_result["power_practical_w"], turbine_rpm)
    
    afg_design = wind_module.design_afg_generator(
        target_voltage.value, 
        generator_rpm
    )
    
    wire_heating = wind_module.calculate_wire_heating(current, wire_diameter * 1e-3)
    
    # Solar & Battery Module
    solar_module = SolarBatteryModule()
    battery_result = solar_module.calculate_battery_capacity(load_params)
    solar_recommendation = solar_module.recommend_solar_panel(
        battery_result["practical_capacity_ah"],
        target_voltage.value,
        solar_params,
        autonomy_days
    )
    
    # System Advisor
    advisor = SystemAdvisor()
    
    # Inverter loss (only for 220V)
    inverter_result = None
    if target_voltage == VoltageTarget.V220:
        inverter_result = advisor.calculate_inverter_loss(total_watts)
    
    # Voltage drop
    vdrop_result = advisor.calculate_voltage_drop(
        current, cable_distance, wire_diameter * 1e-3, target_voltage.value
    )
    
    # Voltage upgrade recommendation
    voltage_upgrade = advisor.recommend_voltage_upgrade(target_voltage, vdrop_result["voltage_drop_percent"])
    
    # System compatibility
    compatibility = advisor.system_compatibility_check(
        wind_result["power_practical_w"],
        solar_recommendation["recommended_wp"] * 0.8,  # Assume 80% of rated
        total_watts
    )
    
    # Reality Check
    reality = RealityCheck.check_feasibility(
        wind_result, battery_result, vdrop_result, compatibility
    )
    
    # =================================================================
    # MAIN DISPLAY - RESULTS
    # =================================================================
    
    # Reality Check Banner
    st.markdown('<div class="section-header">🔍 Physical Reality Check</div>', unsafe_allow_html=True)
    render_reality_badge(reality)
    
    if reality["issues"]:
        with st.expander("🚨 Masalah Kritis"):
            for issue in reality["issues"]:
                st.error(issue)
    
    if reality["warnings"]:
        with st.expander("⚠️ Peringatan"):
            for warning in reality["warnings"]:
                st.warning(warning)
    
    with st.expander("💡 Rekomendasi"):
        for rec in reality["recommendations"]:
            st.info(rec)
    
    # System Overview Metrics
    st.markdown('<div class="section-header">📊 Ikhtisar Sistem</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Daya Angin (Praktis)",
            value=f"{wind_result['power_practical_w']:.1f} W",
            delta=f"Teoritis: {wind_result['power_theoretical_w']:.1f} W"
        )
    
    with col2:
        st.metric(
            label="Kapasitas Baterai",
            value=f"{battery_result['practical_capacity_ah']:.0f} Ah",
            delta=f"{battery_result['required_capacity_ah']:.1f} Ah teoritis"
        )
    
    with col3:
        st.metric(
            label="Panel Surya (WP)",
            value=f"{solar_recommendation['recommended_wp']:.0f} Wp",
            delta=f"{solar_recommendation['num_panels']}×{solar_recommendation['standard_panel_wp']}W"
        )
    
    with col4:
        daily_energy = total_watts * usage_hours
        st.metric(
            label="Energi Harian",
            value=f"{daily_energy:.0f} Wh",
            delta=f"{daily_energy/1000:.2f} kWh"
        )
    
    # Wind & AFG Results
    st.markdown('<div class="section-header">🌬️ Modul Angin & Generator AFG</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Daya Turbin Angin")
        
        # Status
        render_traffic_light(
            wind_result["status"],
            f"Status: {wind_result['status'].upper()}"
        )
        
        st.markdown(f"""
        <div class="result-card">
        <b>Area Sapuan:</b> {wind_result['swept_area_m2']:.2f} m²<br>
        <b>Daya Teoritis (Betz):</b> {wind_result['power_theoretical_w']:.2f} W<br>
        <b>Daya Praktis (Cp=0.35):</b> {wind_result['power_practical_w']:.2f} W<br>
        <b>RPM Turbin (TSR=6):</b> {turbine_rpm:.1f} RPM<br>
        <b>Torsi Turbin:</b> {torque_result['torque_nm']:.2f} Nm
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Transmisi & Generator")
        
        render_traffic_light(
            "green" if reducer_result["ratio"] > 1 else "yellow",
            f"Rasio Reducer: {reducer_result['ratio']:.2f}:1"
        )
        
        st.markdown(f"""
        <div class="result-card">
        <b>Rasio Pulley:</b> {reducer_result['ratio']:.2f}:1<br>
        <b>RPM Generator:</b> {generator_rpm:.1f} RPM<br>
        <b>Multiplier Torsi:</b> {reducer_result['torque_multiplier']:.2f}×<br>
        <b>Lilitan Koil:</b> {afg_design['required_turns']} lilitan<br>
        <b>Frekuensi:</b> {afg_design['frequency_hz']:.1f} Hz<br>
        <b>Konstanta Tegangan:</b> {afg_design['voltage_constant']:.3f} V/RPM
        </div>
        """, unsafe_allow_html=True)
    
    # Physics: Betz Limit
    render_physics_card(PhysicsEducation.betz_limit)
    
    # Solar & Battery Results
    st.markdown('<div class="section-header">☀️ Modul Surya & Baterai</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Kapasitas Baterai")
        
        dod_color = "green" if battery_result['dod_limit_percent'] >= 80 else "yellow"
        render_traffic_light(
            dod_color,
            f"DoD: {battery_result['dod_limit_percent']:.0f}% ({battery_type.value})"
        )
        
        st.markdown(f"""
        <div class="result-card">
        <b>Energi Harian:</b> {battery_result['daily_energy_wh']:.0f} Wh<br>
        <b>Energi Total ({autonomy_days} hari):</b> {battery_result['total_energy_needed_wh']:.0f} Wh<br>
        <b>Kapasitas Dibutuhkan:</b> {battery_result['required_capacity_ah']:.1f} Ah @ {battery_result['system_voltage_v']}V<br>
        <b>Kapasitas Praktis:</b> {battery_result['practical_capacity_ah']:.0f} Ah<br>
        <b>Energi Tersedia:</b> {battery_result['usable_energy_wh']:.0f} Wh (DoD {battery_result['dod_limit_percent']:.0f}%)<br>
        <b>Sel Seri:</b> {battery_result['cells_series']} sel
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Rekomendasi Panel Surya")
        
        render_traffic_light(
            "green" if solar_recommendation['estimated_recharge_days'] <= 2.5 else "yellow",
            f"Waktu Cas: {solar_recommendation['estimated_recharge_days']:.1f} hari"
        )
        
        st.markdown(f"""
        <div class="result-card">
        <b>WP Dibutuhkan:</b> {solar_recommendation['required_wp']:.0f} Wp<br>
        <b>Rekomendasi:</b> {solar_recommendation['recommended_wp']:.0f} Wp<br>
        <b>Konfigurasi:</b> {solar_recommendation['num_panels']}×{solar_recommendation['standard_panel_wp']}W panel<br>
        <b>Energi Harian Panel:</b> {solar_recommendation['recommended_wp'] * sun_hours:.0f} Wh<br>
        <b>Efisiensi Cas:</b> {solar_recommendation['charge_efficiency']*100:.0f}%
        </div>
        """, unsafe_allow_html=True)
    
    # System Advisor Results
    st.markdown('<div class="section-header">🎯 System Advisor</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Voltage Drop")
        
        render_traffic_light(
            vdrop_result["color"],
            f"Drop: {vdrop_result['voltage_drop_percent']:.2f}%"
        )
        
        st.markdown(f"""
        <div class="result-card">
        <b>Arus:</b> {vdrop_result['current_a']:.2f} A<br>
        <b>Hambatan Kabel:</b> {vdrop_result['resistance_ohm']:.4f} Ω<br>
        <b>V_drop:</b> {vdrop_result['voltage_drop_v']:.2f} V<br>
        <b>Tegangan Tersisa:</b> {vdrop_result['remaining_voltage_v']:.2f} V<br>
        <b>Status:</b> {vdrop_result['status'].upper()}
        </div>
        """, unsafe_allow_html=True)
        
        if voltage_upgrade:
            st.warning(f"💡 Disarankan upgrade ke {voltage_upgrade.value}V untuk mengurangi voltage drop!")
    
    with col2:
        st.subheader("Pemanasan Kabel")
        
        render_traffic_light(
            wire_heating["color"],
            f"Status: {wire_heating['status'].upper()}"
        )
        
        st.markdown(f"""
        <div class="result-card">
        <b>Daya Panas:</b> {wire_heating['power_dissipation_w_per_m']:.3f} W/m<br>
        <b>Kenaikan Suhu:</b> {wire_heating['temperature_rise_c']:.1f}°C<br>
        <b>Suhu Akhir:</b> {wire_heating['final_temperature_c']:.1f}°C<br>
        <b>Limit PVC:</b> {wire_heating['pvc_limit_c']}°C<br>
        <b>Density Arus:</b> {wire_heating['current_density_a_mm2']:.2f} A/mm²
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.subheader("Keseimbangan Sistem")
        
        render_traffic_light(
            compatibility["color"],
            compatibility["status"].upper()
        )
        
        st.markdown(f"""
        <div class="result-card">
        <b>Daya Angin:</b> {compatibility['wind_power_w']:.1f} W<br>
        <b>Daya Surya:</b> {compatibility['solar_power_w']:.1f} W<br>
        <b>Total Generasi:</b> {compatibility['total_generation_w']:.1f} W<br>
        <b>Beban:</b> {compatibility['load_watts']:.0f} W<br>
        <b>Margin:</b> {compatibility['margin_percent']:.1f}%
        </div>
        """, unsafe_allow_html=True)
        
        st.info(compatibility["message"])
    
    # Inverter section (only for 220V)
    if inverter_result:
        st.subheader("Konversi Inverter (DC → AC)")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Daya DC Input",
                f"{inverter_result['dc_power_w']:.0f} W"
            )
        with col2:
            st.metric(
                "Daya AC Output",
                f"{inverter_result['ac_power_w']:.0f} W",
                delta=f"-{inverter_result['loss_w']:.0f} W ({inverter_result['loss_percent']:.0f}% loss)"
            )
    
    # Physics Education Section
    st.markdown('<div class="section-header">📚 Physics Insights (The Noob-less Part)</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_physics_card(PhysicsEducation.faraday_law)
        render_physics_card(PhysicsEducation.ohm_law)
    
    with col2:
        render_physics_card(PhysicsEducation.joule_law)
    
    # Summary
    st.markdown('<div class="section-header">📝 Ringkasan Desain</div>', unsafe_allow_html=True)
    
    summary_data = {
        "Parameter": [
            "Status Kelayakan",
            "Daya Angin (Praktis)",
            "Panel Surya (Rekomendasi)",
            "Kapasitas Baterai",
            "Tegangan Sistem",
            "Voltage Drop",
            "Hari Autonomi",
            "Energi Harian"
        ],
        "Nilai": [
            reality["status"],
            f"{wind_result['power_practical_w']:.1f} W",
            f"{solar_recommendation['recommended_wp']:.0f} Wp ({solar_recommendation['num_panels']} panel)",
            f"{battery_result['practical_capacity_ah']:.0f} Ah @ {target_voltage.value}V",
            f"{target_voltage.value}V",
            f"{vdrop_result['voltage_drop_percent']:.2f}%",
            f"{autonomy_days} hari",
            f"{total_watts * usage_hours:.0f} Wh"
        ]
    }
    
    st.table(summary_data)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #636e72; padding: 20px;">
        <b>ElectroNoob-less: Independent Power Architect v1.0</b><br>
        Dibangun berdasarkan hukum fisika: Faraday, Ohm, Joule, dan Betz<br>
        <i>"From Noob to Know - Desain energi mandiri dengan dasar ilmiah"</i>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
