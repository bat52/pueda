#include <stdlib.h>
#include <iostream>
#include <verilated.h>

#if VM_TRACE
    #ifdef DUMP_FST
        #include <verilated_fst_c.h>
        #define DUMP_TYPE VerilatedFstC
        #define DUMP_FILE "dump.fst"
    #else
        #include <verilated_vcd_c.h>
        #define DUMP_TYPE VerilatedVcdC
        #define DUMP_FILE "dump.vcd"
    #endif
#endif
#include "Vcounter.h"

#ifndef CLK_HALF_PERIOD_DELAY
#define CLK_HALF_PERIOD_DELAY 5
#endif

#ifndef DUMP_LEVEL
#define DUMP_LEVEL 0
#endif

class DutWrapper : public Vcounter{
    public: 
        vluint64_t sim_time = 0;
        DutWrapper();
        ~DutWrapper();

        void release_reset();
        void clock_tick();
        uint8_t read_count();

    private:
        #if VM_TRACE    
        DUMP_TYPE *m_trace;
        #endif
        void half_clock_tick();        
};

void DutWrapper::half_clock_tick()
{
    this->clk ^= 1;
    this->eval();
#if VM_TRACE
    this->m_trace->dump(sim_time);
#endif
    this->sim_time += CLK_HALF_PERIOD_DELAY;
}

void DutWrapper::clock_tick()
{
    this->half_clock_tick();
    this->half_clock_tick();
}

void DutWrapper::release_reset()
{
    // initialize inputs
    this->up_down=0;
    this->load=0;
    this->data=0;
    
    this->reset = 1; // reset
    this->clock_tick();
    this->half_clock_tick(); // asynchronous

    this->reset = 0;
    this->clock_tick();
    // this->clock_tick();

}

DutWrapper::DutWrapper()
{
    #if VM_TRACE
        Verilated::traceEverOn(true);
        this->m_trace = new DUMP_TYPE;
        this->trace(this->m_trace, DUMP_LEVEL);
        this->m_trace->open(DUMP_FILE);
    #endif

    this->release_reset();
}

DutWrapper::~DutWrapper()
{
#if VM_TRACE
    m_trace->close();
    delete m_trace;
#endif
}

uint8_t DutWrapper::read_count()
{
    return this->count;
}

/////////////// C-style access

DutWrapper *dut;

void dut_init(){
    dut = new DutWrapper;
}

void dut_close(){
    delete dut;
}

uint32_t read_count()
{
    return dut->read_count();
}

void clock_tick()
{
    dut->clock_tick();
}