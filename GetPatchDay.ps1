<#
    *OVERVIEW 
    This script finds the date of an instance of a weekday in the current/given month.

    In this particular case, the script will output the second Tuesday of the month (patch tuesday) by default.
    - Optionally, you can pass in a week day and an instance count to find what date that day falls on.

    *EXPECTED OUTPUTS
    The date of patch Tuesday.
    
    - If given optional parameters, it will find the “X” instance of given day of the week.
        Changing the $weekDay and $findNthDay parameters give your desired outputs/outcomes.
        e.g To get the 2nd wednesday of the month; under Param(), change $weekDay to Wednesday and $findNthDay to 2.

    *TESTS
        # Get Patch Tuesday for the month
    Get-PatchDay
        # Is today Patch Tuesday?
    (get-date).Day -eq (Get-PatchDay).day
        # Get 5 days after patch Tuesday
    (Get-PatchDay).AddDays(5)
        # Get the 3rd wednesday of the month
    Get-PatchDay -weekDay Thursday -findNthDay 3 
        # Get the 3rd wednesday of particular month e.g July
    Get-PatchDay -weekDay Thursday -findNthDay 3 -month 7
#>

#-------------------{Execution Context}--------------------

Function Get-PatchDay {
    [CmdletBinding()]
    Param (
      [Parameter(position = 0)]
      [ValidateSet("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")]
      [String]$weekDay = 'Tuesday',
      [Parameter(position = 1)]
      [ValidateRange(0, 5)]
      [int]$findNthDay = 2,
      [Parameter(position = 1)]
      [ValidateRange(0, 12)]
      [int]$month = 6
    )
    
    # Get the date; current month, year and first day of the month
    [datetime]$today = [datetime]::NOW
        <# 
            $todayM = $today.Month.ToString() # Current Month using datetime
            $todayM = (($today.Month) + 1).ToString() # incrementing for "Next Month" using datetime
        #> 

    $patchM = $month.ToString() # Patch Month using $month params
    $todayY = $today.Year.ToString() # Current Year
    [datetime]$strtMonth = $patchM + '/1/' + $todayY # First Day

    # Find the first instance of the given weekday using [datetime] methods
    while ($strtMonth.DayofWeek -ine $weekDay) { # "-ine" = (case insensitive) not equals check
        $strtMonth = $strtMonth.AddDays(1) 
    } 
    $firstWeekDay = $strtMonth
  
    <#  
        Identify, calculate the no_ of day(s) to offset per nth instance of weekday 
        i.e If NthDay = 1, dayOffset = 0, (cos we'd be looking for the 1st instance)
               NthDay = 2, dayOffset = 7 (cos 7days = 1 week) etc...
    #>
    if ($findNthDay -eq 1) { # "-eq" = equals check
      $dayOffset = 0
    }
    else {  
      $dayOffset = ($findNthDay - 1) * 7
    }
    
    # Return date of day/instance specified
    $patchTuesday = $firstWeekDay.AddDays($dayOffset) 
    return $patchTuesday
}


