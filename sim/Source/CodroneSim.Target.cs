// Fill out your copyright notice in the Description page of Project Settings.

using UnrealBuildTool;
using System.Collections.Generic;

public class CodroneSimTarget : TargetRules
{
	public CodroneSimTarget(TargetInfo Target) : base(Target)
	{
		
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.V6;
		ExtraModuleNames.AddRange( new string[] { "CodroneSim" } );
	}
}
