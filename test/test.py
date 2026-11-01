# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    expected_state = 0x0F
    for i in range(256):
        await ClockCycles(dut.clk, 1)
        actual_state = int(dut.uo_out.value)
        assert actual_state == expected_state, f"On cycle {i+1} expected {expected_state:#x} but got {actual_state:#x}"
        expected_state = ((expected_state << 1) & 0xFF) | (((expected_state >> 3) ^ (expected_state >> 2)) & 0x01)
        
        

