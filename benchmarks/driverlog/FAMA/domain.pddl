(define (domain dlog-3-3-3-problem-problem-domain)
 (:requirements :strips :typing :negative-preconditions :equality)
 (:types
    location locatable - object
    driver truck obj - locatable
 )
 (:predicates (at- ?obj - locatable ?loc - location) (in ?obj1 - obj ?obj-0 - truck) (driving ?d - driver ?v - truck) (link ?x - location ?y - location) (path ?x - location ?y - location) (empty ?v - truck))
 (:action load-truck
  :parameters ( ?o1 - obj ?o2 - truck ?o3 - location ?o4 - obj ?o5 - truck ?o6 - location)
  :precondition (and )
  :effect (and ))
 (:action unload-truck
  :parameters ( ?o1 - obj ?o2 - truck ?o3 - location ?o4 - obj ?o5 - truck ?o6 - location)
  :precondition (and )
  :effect (and ))
 (:action board-truck
  :parameters ( ?o1 - driver ?o2 - truck ?o3 - location ?o4 - driver ?o5 - truck ?o6 - location)
  :precondition (and )
  :effect (and ))
 (:action disembark-truck
  :parameters ( ?o1 - driver ?o2 - truck ?o3 - location ?o4 - driver ?o5 - truck ?o6 - location)
  :precondition (and )
  :effect (and ))
 (:action drive-truck
  :parameters ( ?o1 - truck ?o2 - location ?o3 - location ?o4 - driver ?o5 - truck ?o6 - location ?o7 - location ?o8 - driver)
  :precondition (and )
  :effect (and ))
 (:action walk
  :parameters ( ?o1 - driver ?o2 - location ?o3 - location ?o4 - driver ?o5 - location ?o6 - location)
  :precondition (and )
  :effect (and ))
)
