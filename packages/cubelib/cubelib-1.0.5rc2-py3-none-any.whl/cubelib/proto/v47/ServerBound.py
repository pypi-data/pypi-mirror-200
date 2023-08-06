from ...types import *
from cubelib.p import Night

from cubelib.proto.version_independent.ServerBound import ClassicLogin


class Login(ClassicLogin):
    pass

class Play:

    class KeepAlive(Night):

        KeepAliveID: VarInt

    class ChatMessage(Night):

        Message: String

    class UseEntity(Night):

        Target: VarInt
        Type: VarInt
        TargetX: Optional('Type', 2)[Float]
        TargetY: Optional('Type', 2)[Float]
        TargetZ: Optional('Type', 2)[Float]

    class Player(Night):

        OnGround: Bool

    class PlayerPosition(Night):

        X: Double
        FeetY: Double # Absolute position, normally Head Y - 1.62
        Z: Double
        OnGround: Bool

    class PlayerLook(Night):

        Yaw: Float
        Pitch: Float
        OnGround: Bool

    class PlayerPositionAndLook(Night):

        X: Double
        FeetY: Double
        Z: Double
        Yaw: Float
        Pitch: Float
        OnGround: Bool

    class PlayerDigging(Night):

        Status: PlayerDiggingStatusEnum
        Location: Position
        Face: FaceEnum

    class PlayerBlockPlacement(Night):

        Location: Position
        Face: FaceEnum
        HeldItem: Slot

    class HeldItemChange(Night):

        Slot: Short

    class Animation(Night):
        pass

    class EntityAction(Night):

        EntityID: VarInt
        ActionID: EntityActionActionIDEnum
        ActionParam: VarInt

    class SteerVehicle(Night):

        Sideways: Float
        Forward: Float
        Flags: UnsignedByte

    class CloseWindow(Night):

        WindowID: UnsignedByte

    class ClickWindow(Night):

        WindowID: UnsignedByte
        Slot: Short
        Button: Byte
        ActionNumber: Short
        Mode: Byte
        ClickedItem: Slot

    class ConfirmTransaction(Night):

        WindowID: Byte
        ActionNumber: Short
        Accepted: Bool

    class CreativeInventoryAction(Night):

        Slot: Short
        ClickedItem: Slot

    class EnchantItem(Night):

        WindowID: Byte
        Enchantment: Byte

    class UpdateSign(Night):

        Location: Position
        Line1: String
        Line2: String
        Line3: String
        Line4: String

    class PlayerAbilities(Night):

        Flags: Byte
        FlyingSpeed: Float
        WalkingSpeed: Float

    class TabComplete(Night):

        Text: String
        HasPosition: Bool
        LookedAtBlock: ByteArray

    class ClientSettings(Night):

        Locale: String
        VievDistance: Byte
        ChatMode: Byte
        ChatColors: Bool
        DisplayedSkinParts: UnsignedByte

    class ClientStatus(Night):

        ActionID: VarInt

    class PluginMessage(Night):

        Channel: String
        Data: ByteArray

    class Spectate(Night):

        TargetPlayer: String

    class ResourcePackStatus(Night):

        Hash: String
        Result: VarInt

    map = {
        0x00: KeepAlive,
        0x01: ChatMessage,
        0x02: UseEntity,
        0x03: Player,
        0x04: PlayerPosition,
        0x05: PlayerLook,
        0x06: PlayerPositionAndLook,
        0x07: PlayerDigging,
        0x08: PlayerBlockPlacement,
        0x09: HeldItemChange,
        0x0a: Animation,
        0x0b: EntityAction,
        0x0c: SteerVehicle,
        0x0d: CloseWindow,
        0x0e: ClickWindow,
        0x0f: ConfirmTransaction,
        0x10: CreativeInventoryAction,
        0x11: EnchantItem,
        0x12: UpdateSign,
        0x13: PlayerAbilities,
        0x14: TabComplete,
        0x15: ClientSettings,
        0x16: ClientStatus,
        0x17: PluginMessage,
        0x18: Spectate,
        0x19: ResourcePackStatus
    }
    inv_map = {v: k for k, v in map.items()}
