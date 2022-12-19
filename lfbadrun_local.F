c
c     lfbadrun_b1258.f           28-JUN-1997            Y.Takeuchi
c
c     use 1258d badrun list for R1742-9299
c
c     2004/04/05   modified by Y.Takeuchi
c        o added  badsub.sk2.manual
c     2007/06/08   modified by Y.Takeuchi
c        o added  badsub.sk3.manual
c 
ccccccccccccccccccccccccccccccccccccccccccccccc
      integer function lfbadrun_local(nrun, nsub)
ccccccccccccccccccccccccccccccccccccccccccccccc
c
c     check badrun
c
c     input 
c       nrun ... run number
c       nsub ... sub run number
c
c     return value
c	1 ... badrun
c	0 ... not badrun
c
      implicit none
      integer MAXBAD1
      parameter (MAXBAD1=30000)
      integer  nrun, nsub, i, nrunb(MAXBAD1), nsubb(MAXBAD1),nbad,nbad2
      save nrunb,nsubb,nbad,nbad2
      logical ex
      
c*** for SK-2 (run number > 20000)     
      integer MAXBAD2
      parameter (MAXBAD2=30000)
      integer  nrunb_sk2(MAXBAD2), nsubb_sk2(MAXBAD2),nbad_sk2,nbad2_sk2
      save nrunb_sk2,nsubb_sk2,nbad_sk2,nbad2_sk2

c*** for SK-3 (run number > 30000)     
      integer MAXBAD3
      parameter (MAXBAD3=30000)
      integer  nrunb_sk3(MAXBAD3), nsubb_sk3(MAXBAD3),nbad_sk3,nbad2_sk3
      save nrunb_sk3,nsubb_sk3,nbad_sk3,nbad2_sk3

c*** for SK-4 (run number > 60000)     
      integer MAXBAD4
c      parameter (MAXBAD4=300000)
      parameter (MAXBAD4=500000)
      integer  nrunb_sk4(MAXBAD4), nsubb_sk4(MAXBAD4),nbad_sk4,nbad2_sk4
      save nrunb_sk4,nsubb_sk4,nbad_sk4,nbad2_sk4

c*** for SK-5 (run number > 80000)
      integer MAXBAD5
      parameter (MAXBAD5=5000)
c      parameter (MAXBAD5=500000)
      integer  nrunb_sk5(MAXBAD5), nsubb_sk5(MAXBAD5),nbad_sk5,nbad2_sk5
      save nrunb_sk5,nsubb_sk5,nbad_sk5,nbad2_sk5

c***  for SK-6 (run number > 85000)
      integer MAXBAD6
      parameter (MAXBAD6=10000)
c      parameter (MAXBAD6=500000)
      integer  nrunb_sk6(MAXBAD6), nsubb_sk6(MAXBAD6),nbad_sk6,nbad2_sk6
      save nrunb_sk6,nsubb_sk6,nbad_sk6,nbad2_sk6

      character*200 file_name

      if (nbad.eq.0) then
c
c*** read old badrun file
      call findconsts(file_name,'badsub SK-I 1',
     $        'badsub.sk.r1742-3051.r3208-3608',2)
      open(99,file=file_name,form='formatted',status='old')
c         open(99,
c     $        file='/home/sklowe/const/badsub.sk.r1742-3051.r3208-3608',
c     $        form='formatted',status='old')
 100     continue
            nbad = nbad + 1
            read(99, *, end=110) nrunb(nbad), nsubb(nbad)
         goto 100
 110     continue
         nbad = nbad -1 
         close(99)
         print *, 'nbad 1 = ', nbad
c
c*** read real-time badrun file
      call findconsts(file_name,'badsub SK-I 2',
     $        'badsub.sk.realtim',2)
      open(99,file=file_name,form='formatted',status='old')
c         open(99,file='/home/sklowe/const/badsub.sk.realtim',
c     &        form='formatted',status='old')
 120     continue
            nbad = nbad + 1
            read(99, *, end=130) nrunb(nbad), nsubb(nbad)
         goto 120
 130     continue
         close(99)
         nbad = nbad -1 
         print *, 'nbad 2 = ', nbad
         nbad2 = nbad
c
c*** read manual badrun file
      call findconsts(file_name,'badsub SK-I 3',
     $        'badsub.sk.manual.1260day',2)
      open(99,file=file_name,form='formatted',status='old')
c         open(99,file='/home/sklowe/const/badsub.sk.manual.1260day',
c     &        form='formatted',status='old')
 140     continue
            nbad = nbad + 1
            read(99, *, end=150) nrunb(nbad), nsubb(nbad)
            if (nsubb(nbad).ne.0) then
               do 160 i = 1, nbad2
                  if (nrunb(nbad).eq.nrunb(i) 
     $                 .and. nsubb(nbad).eq.nsubb(i)) then
                     nbad = nbad - 1
                     goto 140
                  endif
 160           continue
            endif
         goto 140
 150     continue
         close(99)
         nbad = nbad -1 
         print *, 'nbad 3 = ', nbad
         nbad2 = nbad
c
c*** read manual badrun file (SLE)
      call findconsts(file_name,'badsub SK-I 4',
     $        'badsub.sk.sle.1260day',2)
      open(99,file=file_name,form='formatted',status='old')
c         open(99,file='/home/sklowe/const/badsub.sk.sle.1260day',
c     &        form='formatted',status='old')
 170     continue
            nbad = nbad + 1
            read(99, *, end=180) nrunb(nbad), nsubb(nbad)
            if (nsubb(nbad).ne.0) then
               do 190 i = 1, nbad2
                  if (nrunb(nbad).eq.nrunb(i) 
     $                 .and. nsubb(nbad).eq.nsubb(i)) then
                     nbad = nbad - 1
                     goto 170
                  endif
 190           continue
            endif
         goto 170
 180     continue
         nbad = nbad -1 
         close(99)
         print *, 'nbad 4 = ', nbad
c
c*** read manual badrun file
      call findconsts(file_name,'badsub SK-I 5',
     $        'badsub.sk.manual',2)
      open(99,file=file_name,form='formatted',status='old')
c         open(99,file='/home/sklowe/const/badsub.sk.manual',
c     &        form='formatted',status='old')
 141     continue
            nbad = nbad + 1
            read(99, *, end=151) nrunb(nbad), nsubb(nbad)
ccccc only for R9300- ccccccccccccccccccccccccccc
            if (nrunb(nbad).le.9299) then
ccccccccccccccccccccccccccccccccccccccccccccccccc
               nbad = nbad -1 
               goto 141
            endif
            if (nsubb(nbad).ne.0) then
               do 161 i = 1, nbad2
                  if (nrunb(nbad).eq.nrunb(i) 
     $                 .and. nsubb(nbad).eq.nsubb(i)) then
                     nbad = nbad - 1
                     goto 141
                  endif
 161           continue
            endif
         goto 141
 151     continue
         close(99)
         nbad = nbad -1 
         print *, 'nbad 5 = ', nbad
         nbad2 = nbad
c
c*** read manual badrun file (SLE)
      call findconsts(file_name,'badsub SK-I 6',
     $        'badsub.sk.sle',2)
      open(99,file=file_name,form='formatted',status='old')
c         open(99,file='/home/sklowe/const/badsub.sk.sle',
c     &        form='formatted',status='old')
 171     continue
            nbad = nbad + 1
            read(99, *, end=181) nrunb(nbad), nsubb(nbad)
ccccc only for R9300- ccccccccccccccccccccccccccc
            if (nrunb(nbad).le.9299) then
ccccccccccccccccccccccccccccccccccccccccccccccccc
               nbad = nbad -1 
               goto 171
            endif
            if (nsubb(nbad).ne.0) then
               do 191 i = 1, nbad2
                  if (nrunb(nbad).eq.nrunb(i) 
     $                 .and. nsubb(nbad).eq.nsubb(i)) then
                     nbad = nbad - 1
                     goto 171
                  endif
 191           continue
            endif
         goto 171
 181     continue
         nbad = nbad -1 
         close(99)
         print *, 'nbad 6 = ', nbad
         nbad2 = nbad

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
cccc SK-II
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c
c*** read manual badrun file (SK-II)
      call findconsts(file_name,'badsub SK-II 1',
     $        'badsub.sk2.manual',2)
      open(99,file=file_name,form='formatted',status='old')
c         open(99,file='/home/sklowe/const/badsub.sk2.manual',
c     &        form='formatted',status='old')
 172     continue
            nbad_sk2 = nbad_sk2 + 1
            read(99,*,end=182) nrunb_sk2(nbad_sk2),nsubb_sk2(nbad_sk2)
            if (nsubb_sk2(nbad_sk2).ne.0) then
cc 20090601 y.takeuchi: nbad2_sk2 is not initialized so this should be 0
               do 192 i = 1, nbad2_sk2
                  if (nrunb_sk2(nbad_sk2).eq.nrunb_sk2(i) 
     $                 .and. nsubb_sk2(nbad_sk2).eq.nsubb(i)) then
                     nbad_sk2 = nbad_sk2 - 1
                     goto 172
                  endif
 192           continue
            endif
         goto 172
 182     continue
         nbad_sk2 = nbad_sk2 -1 
         close(99)
         print *, 'nbad_sk2 SK-II 1 = ', nbad_sk2
         nbad2_sk2 = nbad_sk2
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
cccc SK-III
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c
c*** read manual badrun file (SK-III)
         inquire(file='badsub.sk3.manual', exist=ex)
         if (ex) then
            print *, 'read local badsub.sk3.manual'
            open(99,file='badsub.sk3.manual',
     &           form='formatted',status='old')
         else
            call findconsts(file_name,'badsub SK-III 1',
     $           'badsub.sk3.manual',2)
            open(99,file=file_name,form='formatted',status='old')
c            open(99,file='/home/sklowe/const/badsub.sk3.manual',
c     &           form='formatted',status='old')
         endif
 272     continue
            nbad_sk3 = nbad_sk3 + 1
            read(99,*,end=282) nrunb_sk3(nbad_sk3),nsubb_sk3(nbad_sk3)
            if (nsubb_sk3(nbad_sk3).ne.0) then
cc 20090601 y.takeuchi: nbad2_sk3 is not initialized so this should be 0
               do 292 i = 1, nbad2_sk3
                  if (nrunb_sk3(nbad_sk3).eq.nrunb_sk3(i) 
     $                 .and. nsubb_sk3(nbad_sk3).eq.nsubb(i)) then
                     nbad_sk3 = nbad_sk3 - 1
                     goto 272
                  endif
 292           continue
            endif
         goto 272
 282     continue
         nbad_sk3 = nbad_sk3 -1 
         close(99)
         print *, 'nbad_sk3 SK-III 1 = ', nbad_sk3
         nbad2_sk3 = nbad_sk3
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
cccc SK-IV
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c
c*** read manual badrun file (SK-IV)
c     inquire(file='badsub.sk4.manual.local', exist=ex)
         inquire(file='badsub.sk4.manual.water', exist=ex)
         if (ex) then
c            print *, 'read local badsub.sk4.manual.local'
c     open(99,file='badsub.sk4.manual.local',
            print *, 'read local badsub.sk4.manual.water'
            open(99,file='badsub.sk4.manual.water',
     &           form='formatted',status='old')
         else
ccccccccccccccccccccccccccccccccc
            call findconsts(file_name,'badsub SK-IV',
     $           'badsub.sk4.manual',2)
c            file_name='/disk01/usr5/wanly/lowe/energyrecon/water_t/badsub.sk4.manual.local_20170905'
c            file_name = 'badsub.sk4.manual'
            open(99,file=file_name,form='formatted',status='old')
c            open(99,file='/home/sklowe/const/badsub.sk4.manual',
c     &           form='formatted',status='old')
ccccccccccccccccccccccccccccccccc
         endif
 372     continue
            nbad_sk4 = nbad_sk4 + 1
            read(99,*,end=382) nrunb_sk4(nbad_sk4),nsubb_sk4(nbad_sk4)
            if (nsubb_sk4(nbad_sk4).ne.0) then
cc 20090601 y.takeuchi: nbad2_sk4 is not initialized so this should be 0
               do 392 i = 1, nbad2_sk4
                  if (nrunb_sk4(nbad_sk4).eq.nrunb_sk4(i) 
     $                 .and. nsubb_sk4(nbad_sk4).eq.nsubb(i)) then
                     nbad_sk4 = nbad_sk4 - 1
                     goto 372
                  endif
 392           continue
            endif
         goto 372
 382     continue
         nbad_sk4 = nbad_sk4 -1 
         close(99)
         print *, 'nbad_sk4 SK-IV = ', nbad_sk4
         nbad2_sk4 = nbad_sk4
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
cccc SK-V
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c
c*** read manual badrun file (SK-V)
         inquire(file='badsub.sk5.manual.local', exist=ex)
         if (ex) then
            print *, 'read local badsub.sk5.manual.local'
            open(99,file='badsub.sk5.manual.local',
     &           form='formatted',status='old')
         else
ccccccccccccccccccccccccccccccccc
            call findconsts(file_name,'badsub SK-V',
     $           'badsub.sk5.manual',2)
            file_name = 'badsub.sk5.manual.local'
            open(99,file=file_name,form='formatted',status='old')
ccccccccccccccccccccccccccccccccc
         endif
 472        continue
            nbad_sk5 = nbad_sk5 + 1
            read(99,*,end=482) nrunb_sk5(nbad_sk5),nsubb_sk5(nbad_sk5)
            if (nsubb_sk5(nbad_sk5).ne.0) then
cc 20090601 y.takeuchi: nbad2_sk4 is not initialized so this should be 0
               do 492 i = 1, nbad2_sk5
                  if (nrunb_sk5(nbad_sk5).eq.nrunb_sk5(i)
     $                 .and. nsubb_sk5(nbad_sk5).eq.nsubb(i)) then
                     nbad_sk5 = nbad_sk5 - 1
                     goto 472
                  endif
 492           continue
            endif
         goto 472
 482          continue
         nbad_sk5 = nbad_sk5 -1
         close(99)
         print *, 'nbad_sk5 SK-V = ', nbad_sk5
         nbad2_sk5 = nbad_sk5
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
cccc SK-VI (Gd)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c
c***  read manual badrun file (SK-VI)
         inquire(file='badsub.sk6.manual.local', exist=ex)
         if (ex) then
            print *, 'read local badsub.sk6.manual.local'
            open(99,file='badsub.sk6.manual.local',
     &           form='formatted',status='old')
         else
ccccccccccccccccccccccccccccccccc
            call findconsts(file_name,'badsub SK-VI(Gd)',
     $           'badsub.sk6.manual',2)
            file_name = 'badsub.sk6.manual.local'
            open(99,file=file_name,form='formatted',status='old')
ccccccccccccccccccccccccccccccccc
         endif
 572     continue
         nbad_sk6 = nbad_sk6 + 1
         read(99,*,end=582) nrunb_sk6(nbad_sk6),nsubb_sk6(nbad_sk6)
         if (nsubb_sk6(nbad_sk6).ne.0) then
            do 592 i = 1, nbad2_sk6
               if (nrunb_sk6(nbad_sk6).eq.nrunb_sk6(i)
     $              .and. nsubb_sk6(nbad_sk6).eq.nsubb(i)) then
                  nbad_sk6 = nbad_sk6 - 1
                  goto 572
               endif
 592          continue
            endif
         goto 572
 582     continue
         nbad_sk6 = nbad_sk6 -1
         close(99)
         print *, 'nbad_sk6 SK-VI (Gd) = ', nbad_sk6
         nbad2_sk6 = nbad_sk6
         
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c
c*** check number of badruns
         if (nbad.gt.MAXBAD1) then
            write(0,*) 'lfbadrun:  too many bad runs!! SK-I'
            stop
         endif
         if (nbad_sk2.gt.MAXBAD2) then
            write(0,*) 'lfbadrun:  too many bad runs!! SK-II'
            stop
         endif
         if (nbad_sk3.gt.MAXBAD3) then
            write(0,*) 'lfbadrun:  too many bad runs!! SK-III'
            stop
         endif
         if (nbad_sk4.gt.MAXBAD4) then
            write(0,*) 'lfbadrun:  too many bad runs!! SK-IV'
            stop
         endif
         if (nbad_sk5.gt.MAXBAD5) then
            write(0,*) 'lfbadrun:  too many bad runs!! SK-V'
            stop
         endif
         if (nbad_sk6.gt.MAXBAD6) then
            write(0,*) 'lfbadrun:  too many bad runs!! SK-VI (Gd)'
            stop
         endif
      endif
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c
c*** bad run cut
      if (nrun .lt. 20000) then
         do i = 1, nbad
            if (nrun.eq.nrunb(i) .and. 
     $           (nsubb(i).eq.0 .or. nsub.eq.nsubb(i))) then
               lfbadrun_local = 1
               return
            endif
         enddo
      else if (nrun .lt. 30000) then
         do i = 1, nbad_sk2
            if (nrun.eq.nrunb_sk2(i) .and. 
     $           (nsubb_sk2(i).eq.0 .or. nsub.eq.nsubb_sk2(i))) then
               lfbadrun_local = 1
               return
            endif
         enddo
      else if (nrun .lt. 60000) then
         do i = 1, nbad_sk3
            if (nrun.eq.nrunb_sk3(i) .and. 
     $           (nsubb_sk3(i).eq.0 .or. nsub.eq.nsubb_sk3(i))) then
               lfbadrun_local = 1
               return
            endif
         enddo
c      else 
       else if (nrun .lt. 80000) then
         do i = 1, nbad_sk4
            if (nrun.eq.nrunb_sk4(i) .and. 
     $           (nsubb_sk4(i).eq.0 .or. nsub.eq.nsubb_sk4(i))) then
               lfbadrun_local = 1
               return
            endif
         enddo
c     else
      else if (nrun .lt. 85000) then
         do i = 1, nbad_sk5
            if (nrun.eq.nrunb_sk5(i) .and.
     $           (nsubb_sk5(i).eq.0 .or. nsub.eq.nsubb_sk5(i))) then
               lfbadrun_local = 1
               return
            endif
         enddo
      else 
         do i = 1, nbad_sk6
            if (nrun.eq.nrunb_sk6(i) .and.
     $          (nsubb_sk6(i).eq.0 .or. nsub.eq.nsubb_sk6(i))) then
            lfbadrun_local = 1
            return
         endif
      enddo
      endif

      lfbadrun_local = 0
c
c*** return
      return
      end
