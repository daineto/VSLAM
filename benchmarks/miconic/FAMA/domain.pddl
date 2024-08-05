(define (domain mixed_f8_p4_u0_v0_d0_a0_n0_a0_b0_n0_f0_problem_problem_problem_problem-domain)
 (:requirements :strips :typing :negative-preconditions :equality)
 (:types passenger floor)
 (:predicates (origin ?person - passenger ?floor - floor) (destin ?person - passenger ?floor - floor) (above ?floor1 - floor ?floor2 - floor) (boarded ?person - passenger) (not-boarded ?person - passenger) (served ?person - passenger) (not-served ?person - passenger) (lift-at ?floor - floor))
 (:action board
  :parameters ( ?o1 - floor ?o2 - passenger ?o3 - floor ?o4 - passenger)
  :precondition (and )
  :effect (and ))
 (:action depart
  :parameters ( ?o1 - floor ?o2 - passenger ?o3 - floor ?o4 - passenger)
  :precondition (and )
  :effect (and ))
 (:action up
  :parameters ( ?o1 - floor ?o2 - floor ?o3 - passenger ?o4 - passenger)
  :precondition (and )
  :effect (and ))
 (:action down
  :parameters ( ?o1 - floor ?o2 - floor ?o3 - passenger ?o4 - passenger)
  :precondition (and )
  :effect (and ))
)
