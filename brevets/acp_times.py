"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow # used for date calculations
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.

# https://rusa.org/pages/acp-brevet-control-times-calculator
MIN_SPEEDS = {
    (0, 200): 15,
    (200, 400): 15,
    (400, 600): 15,
    (600, 1000): 11.428,
    (1000, 1300): 13.333
}

MAX_SPEEDS = {
    (0, 200): 34,
    (200, 400): 32,
    (400, 600): 30,
    (600, 1000): 28,
    (1000, 1300): 26
}

FINISH_TIME_LIMITS = {
    200: 810,    # 13:30
    300: 1200,   # 20:00
    400: 1620,   # 27:00
    600: 2400,   # 40:00
    1000: 4500   # 75:00
}

def valid_brevet_distance(brevet_dist_km):
   """
   Args:
      brevet_dist_km: number, the nominal distance of the brevet
         in kilometers, which must be one of 200, 300, 400, 600,
         or 1000 (the only official ACP brevet distances)
   Returns:
      True if the brevet distance is valid, False otherwise
   """
   accepted_brevet_distances = [200, 300, 400, 600, 1000]

   if brevet_dist_km not in accepted_brevet_distances:
      print(f"Accepted brevet distances are: {accepted_brevet_distances}")
      return False
   return True

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
   """
   A function that returns the open time for a control given the distance.

   Args:
      control_dist_km:  number, the control distance in kilometers
      brevet_dist_km: number, the nominal distance of the brevet
         in kilometers, which must be one of 200, 300, 400, 600,
         or 1000 (the only official ACP brevet distances)
      brevet_start_time:  An ISO 8601 format date-time string indicating
         the official start time of the brevet
   Returns:
      An ISO 8601 format date string indicating the control open time.
      This will be in the same time zone as the brevet start time.
   """

   if not valid_brevet_distance(brevet_dist_km):
      raise ValueError(f"Invalid brevet distance: {brevet_dist_km}")
   if control_dist_km > brevet_dist_km:
      raise ValueError(f"Distance exceeds brevet")
   
   offset_minutes = calculate_time_offset_from_start(control_dist_km, is_open_time=True)
   start = arrow.get(brevet_start_time)
   return start.shift(minutes=offset_minutes).isoformat()

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    if not valid_brevet_distance(brevet_dist_km):
        raise ValueError(f"Invalid brevet distance: {brevet_dist_km}")
    if control_dist_km > brevet_dist_km:
        raise ValueError(f"Distance exceeds brevet")
    
    offset_minutes = calculate_time_offset_from_start(control_dist_km, is_open_time=False)
    
    # Apply finish time cap if this is the finish
    if control_dist_km == brevet_dist_km:
        offset_minutes = min(offset_minutes, FINISH_TIME_LIMITS[brevet_dist_km])
    
    start = arrow.get(brevet_start_time)
    return start.shift(minutes=offset_minutes).isoformat()

def determine_speed(control_dist_km, is_open_time=True):
   speeds = MIN_SPEEDS if is_open_time else MAX_SPEEDS
   
   for (lower_bound, upper_bound), speed in speeds.items():
      if lower_bound <= control_dist_km < upper_bound:
         return speed
   
   return None

def calculate_time_offset_from_start(control_dist_km, is_open_time=True):
   """
   Calculate the time offset in minutes from the start for a given control distance.

   Args:
      control_dist_km: number, the control distance in kilometers
      is_open_time: boolean, True if calculating open time, False if calculating close time

   Returns:
      Number of minutes offset from start time
   """
   brackets = [(0, 200), (200, 400), (400, 600), (600, 1000), (1000, 1300)]
   total_minutes = 0
   distance_remaining = control_dist_km
   
   # Open time uses MAX speeds (fastest pace), close time uses MIN speeds (slowest pace)
   speeds_dict = MAX_SPEEDS if is_open_time else MIN_SPEEDS
   
   for start, end in brackets:
      if distance_remaining <= 0:
         break
      
      distance_in_bracket = min(distance_remaining, end - start)
      # Get speed for this bracket from the appropriate dict
      speed = None
      for (lower, upper), spd in speeds_dict.items():
         # Uses the lower bound inclusive and upper bound exclusive for speed brackets
         if lower <= start < upper:
            speed = spd
            break

      # Calculate time for this bracket
      if speed:
         minutes_for_bracket = (distance_in_bracket / speed) * 60
         total_minutes += minutes_for_bracket

      # Subtract the distance we've just accounted for
      distance_remaining -= distance_in_bracket
   
   return total_minutes

def main():

   print(calculate_time_offset_from_start(100, is_open_time=True))

if __name__ == "__main__":
      main()
