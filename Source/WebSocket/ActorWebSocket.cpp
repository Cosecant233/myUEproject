// Fill out your copyright notice in the Description page of Project Settings.


#include "ActorWebSocket.h"
#include "Engine.h"

// Sets default values
AActorWebSocket::AActorWebSocket()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

}

// Called when the game starts or when spawned
void AActorWebSocket::BeginPlay()
{
	Super::BeginPlay();
	
}

// Called every frame
void AActorWebSocket::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

}

void AActorWebSocket::OnConnected()
{
	UE_LOG(LogTemp, Warning, TEXT("%s"), *FString(__FUNCTION__));
	GEngine->AddOnScreenDebugMessage(-1, 5.0f, FColor::Blue, FString::Printf(TEXT("OnConnected")));
	success = true;
}

void AActorWebSocket::OnConnectionError(const FString&Error)
{
	UE_LOG(LogTemp, Warning, TEXT("%s Error:%s"), *FString(__FUNCTION__),*Error);
	GEngine->AddOnScreenDebugMessage(-1, 5.0f, FColor::Blue, FString::Printf(TEXT("OnConnectionError")));
}

void AActorWebSocket::OnClosed(int32 StatusCode, const FString& Reason, bool bWasClean)
{
	UE_LOG(LogTemp, Warning, TEXT("%s StatusCode:%d Reason:%s bWasClean:%d"), *FString(__FUNCTION__), StatusCode, *Reason, bWasClean);
	GEngine->AddOnScreenDebugMessage(-1, 5.0f, FColor::Blue, FString::Printf(TEXT("OnClosed")));
	success = false;
}

void AActorWebSocket::OnMessage(const FString& Message)
{
	UE_LOG(LogTemp, Warning, TEXT("%s Message:%s"), *FString(__FUNCTION__), *Message);
	GEngine->AddOnScreenDebugMessage(-1, 5.0f, FColor::Blue, FString::Printf(TEXT("OnMessage")));
	msg = *Message;
	DataRecv();
}

void AActorWebSocket::OnMessageSent(const FString& MessageString)
{
	UE_LOG(LogTemp, Warning, TEXT("%s MessageString:%s"), *FString(__FUNCTION__), *MessageString);
	GEngine->AddOnScreenDebugMessage(-1, 5.0f, FColor::Blue, FString::Printf(TEXT("OnMessageSent")));
}

void AActorWebSocket::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	Super::EndPlay(EndPlayReason);

	Socket->Close();
}

void AActorWebSocket::MySend()
{
	/*if (Socket->IsConnected())
	{
		Socket->Send(FString::SanitizeFloat(GetGameTimeSinceCreation()));//
        GEngine->AddOnScreenDebugMessage(-1, 5.0f, FColor::Blue, FString::Printf(TEXT("MySend")));
	}*/	
}

void AActorWebSocket::PlayStart()
{
	FModuleManager::Get().LoadModuleChecked("WebSockets");
	GEngine->AddOnScreenDebugMessage(-1, 5.0f, FColor::Blue, FString::Printf(TEXT("BeginPlay")));
	Socket = FWebSocketsModule::Get().CreateWebSocket(ServerURL, ServerProtocol);
	Socket->OnConnected().AddUObject(this, &AActorWebSocket::OnConnected);
	Socket->OnConnectionError().AddUObject(this, &AActorWebSocket::OnConnectionError);
	Socket->OnClosed().AddUObject(this, &AActorWebSocket::OnClosed);
	Socket->OnMessage().AddUObject(this, &AActorWebSocket::OnMessage);
	Socket->OnMessageSent().AddUObject(this, &AActorWebSocket::OnMessageSent);
	Socket->Connect();
	FTimerHandle TimerHandle;
	GetWorldTimerManager().SetTimer(TimerHandle, this, &AActorWebSocket::MySend, 1, true, 1);
}

void AActorWebSocket::MySendData()
{
	if (Socket->IsConnected())
	{
		Socket->Send(SendData);//
	}
}