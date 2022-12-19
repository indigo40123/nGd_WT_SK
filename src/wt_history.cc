#include <fstream>
#include <iostream>
#include <map>
#include <math.h>
#include <sstream>

#include <TCanvas.h>
#include <TDatime.h>
#include <TF1.h>
#include <TFile.h>
#include <TGraphErrors.h>
#include <TH1F.h>
#include <TMath.h>
#include <TObjArray.h>
#include <TProfile.h>
#include <TROOT.h>
#include <TString.h>
#include <TStyle.h>
#include <TSystem.h>

// Number of days for sliding average calculation
#define N_DAY 15

int main(int argc, char *argv[]) {

   gStyle->SetOptFit(111);
   gROOT->ProcessLine("gErrorIgnoreLevel = 1001;");

   // Make a list of elapsed day
   std::map<Int_t, Int_t> elday_run;
   ifstream ifs_elday("/usr/local/sklib_gcc8/skofl-trunk/const/lowe/runsum.dat");
   TString dummy;
   Int_t run_this, elday_this;
   while (ifs_elday >> run_this >> dummy >> dummy >> dummy >> dummy >> dummy >> dummy >> elday_this) {
      elday_run[run_this] = elday_this;
   }

   // Get list of data files
   TString ls_str = gSystem->GetFromPipe("ls output/wt_0*.root");
   TObjArray *tokens = ls_str.Tokenize("\n");

   // Map of profiles
   std::map<Int_t, TProfile *> prof_map;

   // Loop for data files
   printf("Reading data .....\n");
   for (Int_t iData = 0; iData < tokens->GetEntries(); iData++) {
      if (!tokens->At(iData)) {
         continue;
      }

      // Get run number and elapsed day
      TString fname = tokens->At(iData)->GetName();
      TString run_str = fname(fname.Length() - 11, 6);
      run_this = run_str.Atoi();
      if (elday_run.count(run_this) == 0) {
         continue;
      }
      elday_this = elday_run[run_this];
      printf("\r%d/%d runs", iData, tokens->GetEntries());
      fflush(stdout);

      // Get profile
      TFile *ifile = TFile::Open(fname);
      TProfile *prof_this = (TProfile *)ifile->Get("prof");

      // Add to profile for this day
      if (prof_map.count(elday_this) > 0) {
         prof_map[elday_this]->Add(prof_this);
      } else {
         prof_map[elday_this] = (TProfile *)prof_this->Clone();
         prof_map[elday_this]->SetDirectory(0);
      }

      ifile->Close();

   } // End data loop

   // Prepare to draw
   TCanvas *c1 = new TCanvas("c1", "c1", 0, 0, 600, 500);
   c1->Print("test.pdf[");

   // Average profile
   TProfile *prof_avr = (TProfile *)prof_map.begin()->second->Clone();

   // Fit function
   Float_t fit_min = 700, fit_max = 3400;
   TF1 *fexpo = new TF1("fexpo", "[0] + [1]*exp(-x/[2])", fit_min, fit_max);
   fexpo->SetLineColor(2);
   fexpo->SetParLimits(0, 0.4, 0.5);
   fexpo->SetParLimits(2, 8000.0, 30000.0);
   // Graphs
   TGraphErrors *gr_atten = new TGraphErrors();
   TGraphErrors *gr_yield = new TGraphErrors();

   // Loop for elapsed day
   Int_t elday_first = prof_map.begin()->first + floor(N_DAY / 2.);
   Int_t elday_last = prof_map.rbegin()->first - floor(N_DAY / 2.);
   Int_t n_sum = 0;
   printf("\nMerge data and fit .....\n");
   for (Int_t iDay = elday_first; iDay <= elday_last; iDay++) {

      printf("\r%d/%d days", iDay - elday_first, elday_last - elday_first);
      fflush(stdout);

      // Make sum profile
      prof_avr->Reset();
      for (Int_t jDay = 0; jDay < N_DAY; jDay++) {
         elday_this = iDay - floor(N_DAY / 2.) + jDay;
         if (prof_map.count(elday_this) > 0) {
            prof_avr->Add(prof_map[elday_this]);
         }
      }

      // Fit
      fexpo->SetParameters(0, 0.45, 10000.);
      //fexpo->FixParameter(0, 0.0);
      fexpo->FixParameter(1, 0.4457);

      prof_avr->SetTitle(Form("day:%d", iDay));
      prof_avr->Fit(fexpo, "Q0LB", "", fit_min, fit_max);
      gr_atten->SetPoint(gr_atten->GetN(), iDay, fexpo->GetParameter(2) / 100.);
      gr_yield->SetPoint(gr_yield->GetN(), iDay, fexpo->GetParameter(1));

      // Draw
      prof_avr->GetYaxis()->SetRangeUser(0.32, 0.45);
      prof_avr->Draw();
      fexpo->Draw("L same");
      c1->Print("test.pdf");

   } // End elapsed day loop

   printf("\n");

   // Draw graphs
   gr_atten->SetTitle(";elapsed day;attenuation length [m]");
   gr_atten->SetMarkerStyle(20);
   gr_atten->GetYaxis()->SetRangeUser(100, 160);
   gr_atten->Draw("AP");
   c1->Print("test.pdf");
   gr_yield->SetTitle(";elapsed day;light yield [p.e.]");
   gr_yield->SetMarkerStyle(20);
   gr_yield->GetYaxis()->SetRangeUser(0.4, 0.5);
   gr_yield->Draw("AP");

   // Fit with pol1
   TF1 *flin = new TF1("flin", "pol1");
   flin->SetLineColor(2);
   gr_yield->Fit(flin);
   c1->Print("test.pdf");
   c1->Print("test.pdf]");

   // Output text file
   ofstream ofs("wt_new.txt");
   for (Int_t iDay = 0; iDay < gr_atten->GetN(); iDay++) {
      ofs << Form("%d %.1f\n", (Int_t)(gr_atten->GetX()[iDay]),
                  gr_atten->GetY()[iDay] * 100);
   }
   ofs.close();

   // Output graphs
   TFile *ofile = new TFile("gr.root", "RECREATE");
   gr_atten->Write("gr_atten");
   gr_yield->Write("gr_yield");
   ofile->Close();

   return 0;

}
