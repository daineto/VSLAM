(define (domain blocks)
 (:requirements :strips :typing :negative-preconditions :equality)
 (:predicates (on ?o1 - object ?o2 - object) (on-table ?o1 - object) (clear ?o1 - object) (arm-empty) (holding ?o1 - object))
 (:action pickup
  :parameters ( ?o1 - object ?o2 - object ?o3 - object)
  :precondition (and (not (= ?o1 ?o2)) (not (= ?o1 ?o3)) (not (= ?o2 ?o3)))
  :effect (and ))
 (:action putdown
  :parameters ( ?o1 - object ?o2 - object ?o3 - object)
  :precondition (and (not (= ?o1 ?o2)) (not (= ?o1 ?o3)) (not (= ?o2 ?o3)))
  :effect (and ))
 (:action stack
  :parameters ( ?o1 - object ?o2 - object ?o3 - object)
  :precondition (and (not (= ?o1 ?o2)) (not (= ?o1 ?o3)) (not (= ?o2 ?o3)))
  :effect (and ))
 (:action unstack
  :parameters ( ?o1 - object ?o2 - object ?o3 - object)
  :precondition (and (not (= ?o1 ?o2)) (not (= ?o1 ?o3)) (not (= ?o2 ?o3)))
  :effect (and ))
)
