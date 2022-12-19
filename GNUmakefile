#

include $(SKOFL_ROOT)/config.gmk
LOCAL_LIBS	= lfbadrun_local.o -lsklowe_7.0 -lsollib_4.0 -lwtlib_5.1 -lbonsai_3.3 

SRCS = $(wildcard src/*.cc)
TARGETS = $(basename $(subst src,bin,$(SRCS)))

all: lfbadrun_local.o $(TARGETS) 

bin/%: src/%.cc
	$(info ===== Compiling $* =====)
	$(CXX) $(CXXFLAGS) -c src/$*.cc -o obj/$*.o
	LD_RUN_PATH=$(SKOFL_LIBDIR):$(A_LIBDIR) $(CXX) $(CXXFLAGS) -o bin/$* obj/$*.o $(LDLIBS) 

clean: 
	$(RM) bin/* obj/*


