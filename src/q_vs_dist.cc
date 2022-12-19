#include "fortran_interface.h"
#undef MAXPM
#undef MAXPMA
#undef MAXHWSK
#include "skheadC.h"
#include "skparmC.h"
#include "geopmtC.h"
#include "skbadcC.h"
#include "geotnkC.h"

#include <fstream>
#include <sstream>
#include <cmath>

#include <TTree.h>
#include <TVector3.h>
#include <TMath.h>
#include <TProfile.h>
#include <TFile.h>

#define CWATER 21.58333

int BasicReduction(Header *HEAD){

  //
  // basic reduction (see also skhead.h)
  //

  int ireduc = 0;

  // require TQ
  if(!(HEAD->ifevsk & 1)){
    std::cout << " No QBEE TQ " << std::endl;
    ireduc++;
  }
  // require TRG
  if(!(HEAD->ifevsk & (1<<1))){
    std::cout << " No HARD TRG " << std::endl;
    ireduc++;
  }
  // skip pedestal
  if(HEAD->ifevsk & (1<<9) || HEAD->idtgsk & (1<<30)){
    std::cout << " Pedestal " << std::endl;
    ireduc++;
  }
  // skip slow data
  if(HEAD->ifevsk & (1<<14)){
    std::cout << " slow data " << std::endl;
    ireduc++;
  }
  // skip run info
  if(HEAD->ifevsk & (1<<15)){
    std::cout << " run info " << std::endl;
    ireduc++;
  }
  // spacer
  if(HEAD->ifevsk & (1<<19)){
    std::cout << " Remove spacer " << std::endl;
    ireduc++;
  }
  // incomplete
  if(HEAD->ifevsk & (1<<20)){
    std::cout << " Incomplete " << std::endl;
    ireduc++;
  }
  // LED burst
  if(HEAD->ifevsk & (1<<26)){
    std::cout << " LED burst " << std::endl;
    ireduc++;
  }
  // skip inner off
  if(HEAD->ifevsk & (1<<28)){
    std::cout << " inner off " << std::endl;
    ireduc++;
  }
  // require EVNT_HDR
  if(!(HEAD->ifevsk & (1<<31))){
    std::cout << " No EVNT_HDR " << std::endl;
    ireduc++;
  }
  // skip event number zero
  if(HEAD->nevsk == 0){
    std::cout << " event number zero " << std::endl;
    ireduc++;
  }
  //if(ireduc != 0) cout << " event #" << HEAD->nevsk << " is skipped because of the above reasons" << endl;

  return ireduc;
}


//import Fortran functions
extern "C" {
   void geoset_();
   void skoptn_(const char *, int);
   void skbadopt_(int*);
   void skbadch_(int*, int*, int*);
   int lfbadrun_local_(int*, int*);
   void lfmaxrgn_(float*, int*, float*, int*, int*);
   void skdark_(int*, int*);
   void lfhitgeom_sk4_final_(float*, float*, int*, float*, float*, float*, float*, float*);
   void lfoccor_4_(float*, int*, float*, int*, float*);
   float skcoverage_barrel_(float*, float*);
   float skcoverage_sk4_final_(float*, float*);
   void crstnksk_(float*, float*, float*, float*, int*, int*, int*, float*);
}

int main (int argc, char* argv[]) {
	
   // Parameter settings
   Int_t badopt = 55;  
   std::string opt = "31,30,25";  
   Float_t c_gain = 0.0;
   std::string file_gain = "/usr/local/sklib_gcc8/skofl-trunk/const/water.ave10.2";
   std::string file_pmtprod = "/usr/local/sklib_gcc8/skofl-trunk/const/pmt_prod_year_sk5.dat";
   //std::string file_qe = "/usr/local/sklib_gcc8/skofl-trunk/const/qetable5_2.dat";
   std::string file_qe = "/disk02/usr6/iekikei/tba/mc/trunk/qetable_DETSIM_5.dat";
   std::string file_nGdwt = "/disk02/usr7/licheng/nGd_gitlab/Wt_run_D7.txt";
   std::string file_nGdwtyf = "/disk02/usr7/licheng/nGd_gitlab/Wt_run_D7y.txt";
   std::string file_Muwtyf = "/disk02/usr7/licheng/nGd_gitlab/WT_Mu_D7.txt";
   // Check arguments
   if (argc < 3) {
      std::cerr << "Usage: ./bin/q_vs_dist [output file] [input file]" << std::endl;
      exit(1);
   }

   // Get arguments
   std::string file_out = argv[1];
   std::string file_in = argv[2];
   std::cout << "Output file: "  << file_out << " input file:" << file_in << std::endl;

   // Get tree manager
   SuperManager* Smgr = SuperManager::GetManager(); 
   Smgr->CreateTreeManager(10, "\0", "\0", 2);  
   TreeManager* mgr = Smgr->GetTreeManager(10);

   // Open an input file
   mgr->SetInputFile(file_in.c_str());
   mgr->Initialize();

   // Prepare input tree
   TTree* tree = mgr->GetTree();
   Header   *HEAD   = mgr->GetHEAD();
   TQReal   *TQREAL = mgr->GetTQREALINFO();
   LoweInfo *LOWE   = mgr->GetLOWE();
   MuInfo   *MU     = mgr->GetMU();
   tree->SetBranchStatus("*", 0);
   tree->SetBranchStatus("HEADER");
   tree->SetBranchStatus("TQREAL");
   tree->SetBranchStatus("LOWE");
   tree->SetBranchStatus("MU");
	
   // Generate output file
   TFile* ofile = new TFile(file_out.c_str(), "RECREATE");
   TProfile* prof = new TProfile("prof", ";distance [cm];charge [p.e.]", 20, 500, 3500);
   TProfile* thef1 = new TProfile("thef1", ";diretion [theta];charge [p.e.]", 10, -1.01, 1.01);
   TProfile* thef2 = new TProfile("thef2", ";diretion [theta];charge [p.e.]", 10, -1.01, 1.01);
   TProfile* thef3 = new TProfile("thef3", ";diretion [theta];charge [p.e.]", 10, -1.01, 1.01);
   TProfile* thef4 = new TProfile("thef4", ";diretion [theta];charge [p.e.]", 10, -1.01, 1.01);
   TProfile* thef5 = new TProfile("thef5", ";diretion [theta];charge [p.e.]", 10, -1.01, 1.01);

   TProfile* phif1 = new TProfile("phif1", ";diretion [phi];charge [p.e.]", 40, -4.04, 4.04);
   TProfile* phif2 = new TProfile("phif2", ";diretion [phi];charge [p.e.]", 40, -4.04, 4.04);
   TProfile* phif3 = new TProfile("phif3", ";diretion [phi];charge [p.e.]", 40, -4.04, 4.04);
   TProfile* phif4 = new TProfile("phif4", ";diretion [phi];charge [p.e.]", 40, -4.04, 4.04);
   TProfile* phif5 = new TProfile("phif5", ";diretion [phi];charge [p.e.]", 40, -4.04, 4.04);
   // Get run number
   tree->GetEntry(0);
   Int_t run_this = HEAD->nrunsk;

   // Set geometry
   skheadg_.sk_geometry = 6;
   if (run_this < 85000) {
      skheadg_.sk_geometry = 5;
   }
   printf("SK geometry setting: %d\n", skheadg_.sk_geometry);
   geoset_();

   // PMT position vector
   TVector3 v_pm[MAXPM];
   for (Int_t iPM=0; iPM<MAXPM; iPM++) {
      v_pm[iPM].SetXYZ(geopmt_.xyzpm[iPM][0], geopmt_.xyzpm[iPM][1], geopmt_.xyzpm[iPM][2]);
   }

   // Set badch to ibad array
   skbadopt_(&badopt);
   Int_t iret, sub=1;
   skbadch_(&run_this, &sub, &iret);
	
   // Get gain of this run
   ifstream ifs_gain(file_gain);
   std::string line, dummy;
   Float_t gain_run[5];
   Int_t run_line;
   while (std::getline(ifs_gain, line)) {
      std::stringstream ss(line);
      ss >> run_line;
      if (run_line < run_this) {
	 continue;
      } else {
	 for (Int_t iVar=0; iVar<15; iVar++) {
	    ss >> dummy;
	 }
	 for (Int_t iProd=0; iProd<5; iProd++) {
	    ss >> gain_run[iProd];
	 }
	 break;
      }
   }

   // Get water tranparency of this run
   ifstream ifs_nGdwt(file_nGdwt);
   std::string line2, dummy2;
   Float_t GdWt;
   Int_t run_line2;
   while (std::getline(ifs_nGdwt, line2)) { 
     std::stringstream sss(line2);
     sss >> run_line2;
     if (run_line2 < run_this) {
	 continue; 
     } else {
	sss >> GdWt;
	break;
     }
   }

   ifstream ifs_nGdwtyf(file_nGdwtyf);
   std::string line3;
   Float_t GdWtyf;
   Int_t run_line3;
   while (std::getline(ifs_nGdwtyf, line3)) {
     std::stringstream ssss(line3);
     ssss >> run_line3;
     if (run_line3 < run_this) {
         continue;
     } else {
        ssss >> GdWtyf;
        break;
     }
   }

   ifstream ifs_Muwtyf(file_Muwtyf);
   std::string line4;
   Float_t MuWtyf;
   Int_t run_line4;
   while (std::getline(ifs_Muwtyf, line4)) {
     std::stringstream sssss(line4);
     sssss >> run_line4;
     if (run_line4 < run_this) {
         continue;
     } else {
        sssss >> MuWtyf;
        break;
     }
   }
   std::cout<<"==========WT:========== "
	  <<GdWt<<" "<<GdWtyf<<" "<<MuWtyf<<std::endl;        


   // Get produced year of each PMT
   ifstream ifs_prod(file_pmtprod);
   Float_t pmt_prod[MAXPM];
   for (Int_t iPM=0; iPM<MAXPM; iPM++) {
      ifs_prod >> dummy >> pmt_prod[iPM] >> dummy >> dummy >> dummy >> dummy;
   }
	
   // Get gain of each PMT
   Float_t gain[MAXPM];
   Float_t gain_sk4[5] = {0.992057, 1.00184, 0.989083, 0.98216, 0.987678};
   for (Int_t iPM=0; iPM<MAXPM; iPM++) {
      if (pmt_prod[iPM] < 1000) {
	 gain[iPM] = 0;
      } else {
	 Int_t iProd;
	 if (pmt_prod[iPM] < 1996) {
	    iProd = 0;
	 } else if (pmt_prod[iPM] < 1998) {
	    iProd = 1;
	 } else if (pmt_prod[iPM] < 2004) {
	    iProd = 2;
	 } else if (pmt_prod[iPM] < 2005) {
	    iProd = 3;
	 } else {
	    iProd = 4;
	 }
	 gain[iPM] = (gain_run[iProd] - gain_sk4[iProd]) / gain_sk4[iProd];
      }
   }

   // Get dark rate
   Int_t ierr;
   skdark_(&run_this, &ierr);
   Float_t dark_mean = 0.;
   Int_t n_good = 0;
   for (Int_t iPM=0; iPM<MAXPM; iPM++) { 
     if (combad00_.ibad0[iPM]) continue;
     dark_mean += comdark_.dark_rate[iPM];
     n_good++;
   }
   dark_mean /= n_good;
   //std::cout << "dark_mean = " << dark_mean << std::endl;
	
   // Get QE
   ifstream ifs_qe(file_qe);
   Float_t qe[MAXPM];
   for (Int_t iPM=0; iPM<MAXPM; iPM++) {
      ifs_qe >> dummy >> qe[iPM];
   }

   // Prepare variables for event selection
   Int_t mu_event = -1;
   TVector3 v_mu, v_e;

   // SK variables
   int nevsk_parent_mu = -9999;
   int ntrigsk = 0;
   const int max_track = 10;
   float mubentposx[ max_track ] = {0.}; 
   float mubentposy[ max_track ] = {0.}; 
   float mubentposz[ max_track ] = {0.};
   float mubdirx = 0.; 
   float mubdiry = 0.; 
   float mubdirz = 0.;
   int mubstatus   = 0;
   int mubntrack   = 0;
   float spadlt_primary = 0.;
   float spadlt = 0.; float spadlt_tmp = 0.; float spadlt_min_tmp = 0.;
   float spadll = 0.; float spadll_tmp = 0.; float spadll_min_tmp = 0.;
   float diffx[max_track] = {0.}; float diffy[max_track] = {0.}; float diffz[max_track] = {0.};
   float prodx[max_track] = {0.}; float prody[max_track] = {0.}; float prodz[max_track] = {0.};
   float proj[max_track] = {0.};
   float peak_dedx = 0.;

   // Prepare hit arrays
   Float_t tHit[MAXPM];
   Float_t tHit_sort[MAXPM];
   Int_t cabHit[MAXPM];
   Int_t cabHit_sort[MAXPM];
   Int_t index[MAXPM];
   Int_t hit_flag[MAXPM];

   // Prepare segment array
   const Int_t N_SEG = 36;
   Float_t cover_all[N_SEG];
   Float_t cover_alive[N_SEG];
   Float_t q_seg[N_SEG];
   Float_t q_nwt_seg[N_SEG];
   Float_t q_wtc_seg[N_SEG];
   Float_t q_wt_seg[N_SEG];
   Float_t q_wtyf_seg[N_SEG];
   Float_t q_Muwtyf_seg[N_SEG];
   Float_t t_seg[N_SEG];
   Float_t p_seg[N_SEG];
   Float_t num_seg[N_SEG];
   Float_t dist_seg[N_SEG];
   Float_t dark_seg[N_SEG];
   Float_t dark_cor;


   // Total number of events
   Int_t nEvent = tree->GetEntries();
	
   // Main loop 
   for (Int_t iEvent=0; iEvent<nEvent; iEvent++) {
      if ( iEvent % 100000 == 0 ) std::cout << iEvent << "/" << nEvent << std::endl;
	
      // Read an event
      tree->GetEntry(iEvent);

      // Skip bad run
      if ( lfbadrun_local_( &HEAD->nrunsk, &HEAD->nsubsk ) ) {
	 continue;
      }
      
      // Basic reduction
      int ireduc = BasicReduction(HEAD);
      if(ireduc != 0) continue;

      // variables
      ntrigsk  = (TQREAL->it0xsk - HEAD->t0) / 1.92 / 10;
       
      if (HEAD->nevsk > 0) {
      // Event selection, SHE + OD events (muon candidates)
      if ( (ntrigsk == 0) && (HEAD->nevsk != nevsk_parent_mu) 
          &&(HEAD->idtgsk & (1<<28)) && (HEAD->idtgsk & (1<<3)) ) {
	  mubstatus   = MU->muboy_status;
	  mubntrack   = MU->muboy_ntrack;

      // mu direction
      // For multiple muons, it's assumed that all muon directions are parallel.
         mubdirx = MU->muboy_dir[0];
	 mubdiry = MU->muboy_dir[1];
	 mubdirz = MU->muboy_dir[2];
      
      // mu entrance positions
      // initialize
         for ( int itrack = 0; itrack < max_track; itrack++ ){
            mubentposx[ itrack ] = 0.;
            mubentposy[ itrack ] = 0.;
            mubentposz[ itrack ] = 0.;
         }
         for ( int itrack = 0; itrack < mubntrack; itrack++ ) {
            mubentposx[ itrack ] = MU->muboy_entpos[ itrack ][ 0 ];
            mubentposy[ itrack ] = MU->muboy_entpos[ itrack ][ 1 ];
            mubentposz[ itrack ] = MU->muboy_entpos[ itrack ][ 2 ];
         }
      }
      nevsk_parent_mu = HEAD->nevsk;
      if (ntrigsk != 0) {
      // 2nd event selection, SHE + AFT events (neutron candidates)
      if ( ((HEAD->nevsk == nevsk_parent_mu ) && (HEAD->idtgsk & (1<<28)) ) ||
           ((HEAD->nevsk == nevsk_parent_mu + 1 ) && (HEAD->idtgsk & (1<<29)) ) ) {
      
      // Select lowE events in 20-535 us after muon
      if (LOWE->ltimediff > 20*1000 && LOWE->ltimediff < 535*1000 && LOWE->bsn50 > 24) {
	 
	 // calculate dlt
	 for ( int itrack = 0; itrack < max_track; itrack++ ) {
          diffx[ itrack ] = 0.;   diffy[ itrack ] = 0.;   diffz[ itrack ] = 0.;
          prodx[ itrack ] = 0.;   prody[ itrack ] = 0.;   prodz[ itrack ] = 0.;
          proj[ itrack ]  = 0.;
         }
         spadlt = 9999.;
         spadll = 9999.;
	 for ( int itrack = 0; itrack < mubntrack; itrack++ ) {
          diffx[ itrack ] = mubentposx[ itrack ] - LOWE->bsvertex[0];
          diffy[ itrack ] = mubentposy[ itrack ] - LOWE->bsvertex[1];
          diffz[ itrack ] = mubentposz[ itrack ] - LOWE->bsvertex[2];
          prodx[ itrack ] = diffy[ itrack ] * mubdirz - diffz[ itrack ] * mubdiry;
          prody[ itrack ] = diffz[ itrack ] * mubdirx - diffx[ itrack ] * mubdirz;
          prodz[ itrack ] = diffx[ itrack ] * mubdiry - diffy[ itrack ] * mubdirx;
          spadlt_min_tmp  = sqrt( pow(prodx[ itrack ], 2.) + pow(prody[ itrack ], 2.) + pow(prodz[ itrack ], 2.) );
          proj[ itrack ]  = - diffx[ itrack ]*mubdirx - diffy[ itrack ]*mubdiry - diffz[ itrack ]*mubdirz;
	  spadll_min_tmp  = peak_dedx - proj[ itrack ];
          if ( itrack == 0 ) spadlt_primary = spadlt_min_tmp;
          if ( spadlt_min_tmp < spadlt ) spadlt = spadlt_min_tmp;
          if ( spadll_min_tmp < spadll ) spadll = spadll_min_tmp;
        }

	 // Get vertex position 
	 v_e.SetX(LOWE->bsvertex[0]);
	 v_e.SetY(LOWE->bsvertex[1]);
	 v_e.SetZ(LOWE->bsvertex[2]);
	 Float_t r_vtx = sqrt(v_e.X()*v_e.X()+v_e.Y()*v_e.Y());
	 Float_t dist_vtx = (v_e-v_mu).Mag();

	 // Vertex position cut
	 if (fabs(v_e.Z()) < 1610 && r_vtx < 1490 && spadlt < 250) {
             std::cout << "Sec_Event " << HEAD->nevsk << " N50: " << LOWE->bsn50 <<std::endl;
	 // Event quality cut
	 if ( LOWE->bsgood[1] > 0.4 && LOWE->bsdirks < 0.4 ) {
	    // Get time shift
	    Float_t t_shift = (TQREAL->it0xsk - HEAD->t0)/1.92;

	    // Loop for hits
	    Int_t nhit_good = 0;
	    for (Int_t iHit=0; iHit<TQREAL->nhits; iHit++) {

	       // Remove bad ch
	       Int_t cab_this = (TQREAL->cables[iHit] & 0xFFFF);
	       if (combad00_.ibad0[cab_this-1]) {
		  continue;
	       }

	       // Correct TOF and time offset
	       Float_t dist_pm = (v_e - v_pm[cab_this-1]).Mag();
	       Float_t tof = dist_pm/CWATER;

	       // Add to array
	       Float_t t0 = LOWE->bsvertex[3];
	       tHit[nhit_good] = TQREAL->T[iHit] - t_shift - tof - t0;
	       cabHit[nhit_good] = cab_this;
	       nhit_good++;

	    } // End hit loop

	    // Sort hits in time
	    TMath::Sort(nhit_good, tHit, index, false);
	    for (Int_t iHit=0; iHit<nhit_good; iHit++) {
	       tHit_sort[iHit] = tHit[index[iHit]];
	       cabHit_sort[iHit] = cabHit[index[iHit]];
	    }

	    // Find hits in 100 ns time window 
	    Int_t ind[2] = {-1, -1};
	    Float_t t_tail = 100.;
	    for (Int_t iHit=0; iHit<nhit_good; iHit++) {
	       if (ind[0]==-1 && tHit_sort[iHit]>-10) {
		   ind[0] = iHit+1;
	       }
	       if (tHit_sort[iHit]<90) {
		   ind[1] = iHit+1;
	       }
	    }
	    if (ind[0] == -1 || ind[1] == -1) {
	       std::cout << "n100 " << ind[0] << " " << ind[1] << " " << nhit_good << std::endl;
	       continue;
	    }
	    Int_t nhit_tail = ind[1] - ind[0] + 1;
	    for (Int_t iHit=0; iHit<nhit_tail; iHit++) {
	       tHit_sort[iHit] = tHit_sort[ind[0]-1+iHit];
	       cabHit_sort[iHit] = cabHit_sort[ind[0]-1+iHit];
	    }

	    // Find hits in 50 ns time window
	    Float_t t_window = 50.;
	    ind[0] = -1;
	    ind[1] = -1;
	    for (Int_t iHit=0; iHit<nhit_tail; iHit++) {
	       if (ind[0]==-1 && tHit_sort[iHit]>-10) {
		   ind[0] = iHit+1;
	       }
	       if (tHit_sort[iHit]<40) {
		   ind[1] = iHit+1;
	       }
	    }
	    if (ind[0] == -1 || ind[1] == -1) {
	       std::cout << "n50 " << ind[0] << " " << ind[1] << " " << nhit_good << std::endl;
	       continue;
	    }
	    Int_t nhit_window = ind[1] - ind[0] + 1;
	    for (Int_t iHit=0; iHit<nhit_window; iHit++) {
	       tHit_sort[iHit] = tHit_sort[ind[0]-1+iHit];
	       cabHit_sort[iHit] = cabHit_sort[ind[0]-1+iHit];
	    }

	    // Mark selected hits
	    for (Int_t iPM=0; iPM<MAXPM; iPM++) {
	       hit_flag[iPM] = 0;
	    }
	    for (Int_t iHit=0; iHit<nhit_window; iHit++) {
	       hit_flag[cabHit_sort[iHit]-1] = 1;
	    }

	    // Make vectors for calculating phi segment
	    TVector3 v_dir(LOWE->bsdir[0], LOWE->bsdir[1], LOWE->bsdir[2]);
	    TVector3 v_z(0,0,1);
	    TVector3 v_phi0 = v_dir.Cross(v_z).Unit();
	    TVector3 v_base = v_dir.Cross(v_phi0).Unit();
	    TVector3 v_seg = v_dir;
	    v_seg.Rotate(42.0*TMath::Pi()/180., v_base);
	    v_seg.Rotate(-10*0.5*TMath::Pi()/180., v_dir);

	    // Initialize segment arrays
	    for (Int_t iSeg=0; iSeg<N_SEG; iSeg++) { 

	       // Direction vector to the segment
	       Float_t dir_xyz[3];
	       v_seg.Rotate(10*TMath::Pi()/180., v_dir);
	       v_seg.GetXYZ(dir_xyz);

	       // Crossing point of the segment
	       Float_t cross_pos[3];
	       Int_t NORF, IC, IN;
	       Float_t zpintk = ZPINTK;
	       Float_t rintk = RINTK;
	       crstnksk_(LOWE->bsvertex, dir_xyz, &zpintk, &rintk, &NORF, &IC, &IN, cross_pos);

	       // Distance to the segment
	       TVector3 v_cross(cross_pos[0], cross_pos[1], cross_pos[2]);
	       dist_seg[iSeg] = (v_e - v_cross).Mag();
	       t_seg[iSeg] = v_seg.CosTheta();
               p_seg[iSeg] = v_seg.Phi();

	    } // End segment loop

	    // Initialize charge sum and coverage 
	    for (Int_t iSeg=0; iSeg<N_SEG; iSeg++) { 
	       q_seg[iSeg] = 0;
	       q_nwt_seg[iSeg] = 0;
               q_wtc_seg[iSeg] = 0;
               q_wt_seg[iSeg] = 0;
               q_wtyf_seg[iSeg] = 0;
	       q_Muwtyf_seg[iSeg] = 0;

	       cover_all[iSeg] = 0;
	       cover_alive[iSeg] = 0;
	    }

	    // Loop for PMTs
	    for (Int_t iPM=0; iPM<MAXPM; iPM++) {

	       // Get theta and phi
	       Int_t iCab = iPM+1;
	       Float_t dist, costh, pcospm, ptheta, pphi;
	       lfhitgeom_sk4_final_(LOWE->bsvertex, LOWE->bsdir, &iCab, &dist, &costh, &pcospm, &ptheta, &pphi);
	       // Select PMTs near the ring
	       Float_t angle  = 15.;
	       Float_t cos_min = cos((42.0+angle)/180.0*TMath::Pi());
	       Float_t cos_max = cos((42.0-angle)/180.0*TMath::Pi());
	       if (costh < cos_min || costh > cos_max) {
		  continue;
	       }

	       // Get phi vector
	       TVector3 v_vtx2pm = (v_pm[iPM] - v_e).Unit();
	       TVector3 v_phi = (v_vtx2pm - costh*v_dir).Unit();

	       // Get phi segment index
	       Float_t phi_this = v_phi0.Angle(v_phi) * 180. / TMath::Pi();
	       if (v_phi.Dot(v_base) < 0) {
		  phi_this = 360.0 - phi_this;
	       }
	       Int_t phi_seg = (Int_t)(phi_this/10);

	       // Calculate coverage 
	       Float_t cover_this = 1.0;
	       if (iPM < 7650){
		   cover_this = 1.0/skcoverage_barrel_(&ptheta, &pphi);
	       } else {
		   cover_this = 1.0/skcoverage_sk4_final_(&ptheta, &pphi);
	       }
	       cover_all[phi_seg] += cover_this;

	       // Skip bad channel
	       if (combad_.ibad[iPM]) {
		  continue;
	       }
	       cover_alive[phi_seg] += cover_this;

	       // Occupancy factor
	       Float_t dummy2[2];
	       Float_t xoccor;
	       lfoccor_4_(dummy2, hit_flag, qe, &iCab, &xoccor);

	       // Dark rate correction factor
	       Int_t n_pmt_total = 11129;
	       Float_t dark_rate = (n_pmt_total-combad00_.nbad0) * dark_mean*1e3;
	       Float_t dark_corr = dark_rate * t_window*1e-9 / nhit_window;

	       // Tail correction factor
	       Float_t tail_corr = ( (nhit_tail-nhit_window) - dark_rate * (t_tail-t_window)*1e-9 ) / nhit_window;

	       // Effective hit (with attenuation correction)
	       Float_t effective_hit = (xoccor + tail_corr) / (1+gain[iPM]*c_gain) * cover_this / qe[iPM] / (1 - 900e-9 * comdark_.dark_rate[iPM]*1e3);

	       // Subtract dark
	       Float_t dark_exp = comdark_.dark_rate[iPM]*1e3 * t_window*1e-9;
	       q_nwt_seg[phi_seg] -= dark_exp * (xoccor + tail_corr) / (1+gain[iPM]*c_gain) * cover_this / qe[iPM] / (1 - 900e-9 * comdark_.dark_rate[iPM]*1e3);
	       q_wtc_seg[phi_seg] -= dark_exp * (xoccor + tail_corr) / (1+gain[iPM]*c_gain) * cover_this / qe[iPM] / (1 - 900e-9 * comdark_.dark_rate[iPM]*1e3);
	       q_wt_seg[phi_seg] -= dark_exp * (xoccor + tail_corr) / (1+gain[iPM]*c_gain) * cover_this / qe[iPM] / (1 - 900e-9 * comdark_.dark_rate[iPM]*1e3);
	       q_wtyf_seg[phi_seg] -= dark_exp * (xoccor + tail_corr) / (1+gain[iPM]*c_gain) * cover_this / qe[iPM] / (1 - 900e-9 * comdark_.dark_rate[iPM]*1e3);
	       q_Muwtyf_seg[phi_seg] -= dark_exp * (xoccor + tail_corr) / (1+gain[iPM]*c_gain) * cover_this / qe[iPM] / (1 - 900e-9 * comdark_.dark_rate[iPM]*1e3);

	       // Skip if no hit
	       if (!hit_flag[iPM]) {
                       continue;
               }

	       //Sum up the Eff_hit for every section
	       q_nwt_seg[phi_seg] += effective_hit;
	       q_wtc_seg[phi_seg] += effective_hit*exp(dist_seg[phi_seg]/16500.);
	       q_wt_seg[phi_seg] += effective_hit*exp(dist_seg[phi_seg]/GdWt);
	       q_wtyf_seg[phi_seg] += effective_hit*exp(dist_seg[phi_seg]/GdWtyf);
	       q_Muwtyf_seg[phi_seg] += effective_hit*exp(dist_seg[phi_seg]/MuWtyf);

	    } // End hit loop

	    // Fill tree 
	    for (Int_t iSeg=0; iSeg<N_SEG; iSeg++) {
	       // Coverage correction
	       if (cover_alive[iSeg] > 0) {
	          q_nwt_seg[iSeg] *= cover_all[iSeg]/cover_alive[iSeg];
                  q_wtc_seg[iSeg] *= cover_all[iSeg]/cover_alive[iSeg];
		  q_wt_seg[iSeg] *= cover_all[iSeg]/cover_alive[iSeg];
		  q_wtyf_seg[iSeg] *= cover_all[iSeg]/cover_alive[iSeg];
		  q_Muwtyf_seg[iSeg] *= cover_all[iSeg]/cover_alive[iSeg];

		  prof->Fill(dist_seg[iSeg], q_wt_seg[iSeg]);

	          thef1->Fill(t_seg[iSeg], q_nwt_seg[iSeg]);
		  thef2->Fill(t_seg[iSeg], q_wtc_seg[iSeg]);
		  thef3->Fill(t_seg[iSeg], q_wt_seg[iSeg]);
		  thef4->Fill(t_seg[iSeg], q_wtyf_seg[iSeg]);
		  thef5->Fill(t_seg[iSeg], q_Muwtyf_seg[iSeg]);
		  std::cout<<"T: "<<t_seg[iSeg]<<" Q: "<<q_wt_seg[iSeg]<<std::endl;
		  phif1->Fill(p_seg[iSeg], q_nwt_seg[iSeg]);
		  phif2->Fill(p_seg[iSeg], q_wtc_seg[iSeg]);
		  phif3->Fill(p_seg[iSeg], q_wt_seg[iSeg]);
		  phif4->Fill(p_seg[iSeg], q_wtyf_seg[iSeg]);
		  phif5->Fill(p_seg[iSeg], q_Muwtyf_seg[iSeg]);
	          }	     
                } // End Fill Tree
               } // End quality cut
	      } // End position cut
	     } // End time cut
	   } // End 2nd event cut
	 } // End further event selection

      } // End event selection
		
   } // End event loop

   printf("\n");

   // Write output file
   ofile->cd();
   prof->Write();
   thef1->Write();
   thef2->Write();
   thef3->Write();
   thef4->Write();
   thef5->Write();
   phif1->Write();
   phif2->Write();
   phif3->Write();
   phif4->Write();
   phif5->Write();
   ofile->Close();
 
   return 0;     
}
