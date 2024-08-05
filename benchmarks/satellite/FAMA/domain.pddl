(define (domain strips-sat-x-1-problem-domain)
 (:requirements :strips :typing :negative-preconditions :equality)
 (:types satellite direction instrument mode)
 (:predicates (on-board ?i - instrument ?s - satellite) (supports ?i - instrument ?m - mode) (pointing ?s - satellite ?d - direction) (power-avail ?s - satellite) (power-on ?i - instrument) (calibrated ?i - instrument) (have-image ?d - direction ?m - mode) (calibration-target ?i - instrument ?d - direction))
 (:action turn-to
  :parameters ( ?o1 - satellite ?o2 - direction ?o3 - direction ?o4 - satellite ?o5 - direction ?o6 - direction)
  :precondition (and )
  :effect (and ))
 (:action switch-on
  :parameters ( ?o1 - instrument ?o2 - satellite ?o3 - instrument ?o4 - satellite)
  :precondition (and )
  :effect (and ))
 (:action switch-off
  :parameters ( ?o1 - instrument ?o2 - satellite ?o3 - instrument ?o4 - satellite)
  :precondition (and )
  :effect (and ))
 (:action calibrate
  :parameters ( ?o1 - satellite ?o2 - instrument ?o3 - direction ?o4 - satellite ?o5 - instrument ?o6 - direction)
  :precondition (and )
  :effect (and ))
 (:action take-image
  :parameters ( ?o1 - satellite ?o2 - direction ?o3 - instrument ?o4 - mode ?o5 - satellite ?o6 - direction ?o7 - instrument ?o8 - mode)
  :precondition (and )
  :effect (and ))
)
