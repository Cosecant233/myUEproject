// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "WebSocketsModule.h"
#include "IWebSocket.h"
#include "ActorWebSocket.generated.h"

UCLASS()
class WEBSOCKET_API AActorWebSocket : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	AActorWebSocket();
	

UPROPERTY(BlueprintReadWrite)
	FString ServerURL;           // = "ws://127.0.0.1:23333"
UPROPERTY(BlueprintReadWrite)
    FString ServerProtocol;      // = "ws"
UPROPERTY(BlueprintReadOnly)
	FString msg;
UPROPERTY(BlueprintReadOnly)
    bool success=false;
UPROPERTY(BlueprintReadWrite)
    FString SendData;

	TSharedPtr<IWebSocket> Socket = nullptr;

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

UFUNCTION(BlueprintCallable,Category="WebSocket")
	void OnConnected();
UFUNCTION(BlueprintCallable, Category = "WebSocket")
	void OnConnectionError(const FString& Error);
UFUNCTION(BlueprintCallable, Category = "WebSocket")
	void OnClosed(int32 StatusCode, const FString& Reason, bool bWasClean);
UFUNCTION(BlueprintCallable, Category = "WebSocket")
	void OnMessage(const FString& Message);
UFUNCTION(BlueprintCallable, Category = "WebSocket")
	void OnMessageSent(const FString& MessageString);

public:	
	// Called every frame
	virtual void Tick(float DeltaTime) override;
UFUNCTION(BlueprintCallable, Category = "WebSocket")
	void MySend();

public:
UFUNCTION(BlueprintImplementableEvent,Category="WebSocket")
    void DataRecv();
UFUNCTION(BlueprintCallable, Category = "WebSocket")
    void PlayStart();
UFUNCTION(BlueprintCallable, Category = "WebSocket")
    void MySendData();

protected:
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
};
