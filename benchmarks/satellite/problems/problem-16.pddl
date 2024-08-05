(define (problem strips_sat_x_1_problem-problem)
 (:domain strips_sat_x_1_problem-domain)
 (:objects
   satellite0 satellite1 satellite2 satellite3 - satellite
   star2 groundstation1 groundstation3 groundstation0 phenomenon4 phenomenon5 star6 phenomenon7 - direction
   instrument0 instrument1 instrument2 instrument3 instrument4 instrument5 instrument6 instrument7 instrument8 instrument9 instrument10 - instrument
   image0 spectrograph1 image2 - mode
 )
 (:init (supports instrument0 image2) (supports instrument0 spectrograph1) (supports instrument0 image0) (calibration_target instrument0 star2) (supports instrument1 image0) (supports instrument1 spectrograph1) (supports instrument1 image2) (calibration_target instrument1 star2) (supports instrument2 image2) (supports instrument2 image0) (supports instrument2 spectrograph1) (calibration_target instrument2 groundstation1) (on_board instrument0 satellite0) (on_board instrument1 satellite0) (on_board instrument2 satellite0) (power_avail satellite0) (pointing satellite0 groundstation3) (supports instrument3 image0) (supports instrument3 image2) (calibration_target instrument3 groundstation0) (on_board instrument3 satellite1) (power_avail satellite1) (pointing satellite1 groundstation1) (supports instrument4 image0) (supports instrument4 image2) (supports instrument4 spectrograph1) (calibration_target instrument4 groundstation1) (supports instrument5 spectrograph1) (supports instrument5 image2) (calibration_target instrument5 star2) (supports instrument6 spectrograph1) (supports instrument6 image2) (supports instrument6 image0) (calibration_target instrument6 groundstation0) (on_board instrument4 satellite2) (on_board instrument5 satellite2) (on_board instrument6 satellite2) (power_avail satellite2) (pointing satellite2 phenomenon7) (supports instrument7 image0) (supports instrument7 image2) (supports instrument7 spectrograph1) (calibration_target instrument7 groundstation3) (supports instrument8 image0) (calibration_target instrument8 groundstation1) (supports instrument9 image2) (supports instrument9 image0) (supports instrument9 spectrograph1) (calibration_target instrument9 groundstation3) (supports instrument10 image2) (calibration_target instrument10 groundstation0) (on_board instrument7 satellite3) (on_board instrument8 satellite3) (on_board instrument9 satellite3) (on_board instrument10 satellite3) (power_avail satellite3) (pointing satellite3 star6))
 (:goal (and (pointing satellite3 phenomenon5) (have_image phenomenon4 spectrograph1) (have_image phenomenon5 image0) (have_image star6 image2) (have_image phenomenon7 image0)))
)
