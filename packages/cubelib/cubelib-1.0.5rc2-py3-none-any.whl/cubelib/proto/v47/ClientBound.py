from ...types import *
from ...p import Night
from cubelib.proto.version_independent.ClientBound import ClassicLogin


class Login(ClassicLogin):
    pass

class Play:

    class JoinGame(Night):

        EntityID: Int
        Gamemode: UnsignedByte
        Dimension: Byte
        Difficulty: UnsignedByte
        MaxPlayers: UnsignedByte
        LevelType: String
        ReducedDebugInfo: Bool

    class PluginMessage(Night):

        Channel: String
        Data: ByteArray

    class ServerDifficulty(Night):

        Difficulty: UnsignedByte

    class SpawnPosition(Night):

        Location: Position

    class UpdateHealth(Night):

        Health: Float
        Food: VarInt
        FoodSaturating: Float
    
    class Respawn(Night):

        Dimension: Int
        Difficulty: UnsignedByte
        Gamemode: UnsignedByte
        LevelType: String

    class PlayerAbilities(Night):

        Flags: Byte
        FlyingSpeed: Float
        FOVModifier: Float

    class ChatMessage(Night):

        Json_Data: String
        Position: Byte

    class KeepAlive(Night):

        KeepAliveID: VarInt

    class PlayerPositionAndLook(Night):

        X: Double
        FeetY: Double
        Z: Double
        Yaw: Float
        Pitch: Float
        Flags: Byte
    
    class HeldItemChange(Night):

        Slot: Byte

    class TimeUpdate(Night):

        WorldAge: Long
        TimeOfDay: Long

    class WindowItems(Night):

        WindowID: UnsignedByte
        Count: Short
        SlotData: ByteArray

    class EntityRelativeMove(Night):

        EntityID: VarInt
        DeltaX: Byte
        DeltaY: Byte
        DeltaZ: Byte
        OnGround: Bool

    class EntityLook(Night):

        EntityID: VarInt
        Yaw: Angle
        Pitch: Angle
        OnGround: Bool

    class EntityLookAndRelativeMove(Night):

        EntityID: VarInt
        DeltaX: Byte
        DeltaY: Byte
        DeltaZ: Byte
        Yaw: Angle
        Pitch: Angle
        OnGround: Bool

    class EntityHeadLook(Night):

        EntityID: VarInt
        HeadYaw: Angle

    class EntityVelocity(Night):

        EntityID: VarInt
        VelocityX: Short
        VelocityY: Short
        VelocityZ: Short

    class EntityStatus(Night):

        EntityID: Int
        EntityStatus: Byte

    class Disconnect(Night):
        Reason: String

    class EntityEquipment(Night):

        EntityID: VarInt
        Slot: Short
        Item: ByteArray  # ?slot
    
    class UseBed(Night):

        EntityID: VarInt
        Location: Position

    class Animation(Night):

        EntityID: VarInt
        Animation: UnsignedByte

    class SpawnPlayer(Night):

        EntityID: VarInt
        PlayerUUID: UUID
        X: Int
        Y: Int
        Z: Int
        Yaw: Angle
        Pitch: Angle
        CurrentItem: Short
        Metatdata: ByteArray # ?metadata
    
    class CollectItem(Night):

        CollectedEntityID: VarInt
        CollectorEntityID: VarInt

    class SpawnObject(Night):

        EntityID: VarInt
        Type: Byte
        X: Int
        Y: Int
        Z: Int
        Pitch: Angle
        Yaw: Angle
        Data: Int
        VelocityX: Optional('Data', 0, equals=False)[Short]
        VelocityY: Optional('Data', 0, equals=False)[Short]
        VelocityZ: Optional('Data', 0, equals=False)[Short]

    class SpawnMob(Night):

        EntityID: VarInt
        Type: UnsignedByte
        X: Int
        Y: Int
        Z: Int
        Yaw: Angle
        Pitch: Angle
        HeadPitch: Angle
        VelocityX: Short
        VelocityY: Short
        VelocityZ: Short
        Metatdata: ByteArray # ?metadata
    
    class SpawnPainting(Night):

        EntityID: VarInt
        Title: String[13]
        Location: Position
        Direction: UnsignedByte

    class SpawnExperienceOrb(Night):

        EntityID: VarInt
        X: Int
        Y: Int
        Z: Int
        Count: Short

    class DestroyEntities(Night):

        EntityIDs: FiniteLengthArray[VarInt]

    class Entity(Night):

        EntityID: VarInt
    
    class EntityTeleport(Night):

        EntityID: VarInt
        X: Int
        Y: Int
        Z: Int
        Yaw: Angle
        Pitch: Angle
        OnGround: Bool

    class AttachEntity(Night):

        EntityID: Int
        VehicleID: Int
        Leash: Bool
    
    class EntityMetadata(Night):

        EntityID: VarInt
        Metatdata: ByteArray
    
    class EntityEffect(Night):

        EntityID: VarInt
        EffectID: Byte
        Amplifier: Byte
        Duration: VarInt
        HideParticles: Bool

    class RemoveEntityEffect(Night):

        EntityID: VarInt
        EffectID: Byte

    class SetExperience(Night):

        ExperienceBar: Float
        Level: VarInt
        TotalExperience: VarInt

    class EntityProperties(Night):

        EntityID: VarInt
        Data: ByteArray
    
    class ChunkData(Night):

        ChunkX: Int
        ChunkZ: Int
        GroundUpCont: Bool
        PrimaryBitMask: UnsignedShort
        Data: FiniteLengthByteArray

    class MultiBlockChange(Night):

        ChunkX: Int
        ChunkZ: Int
        Data: ByteArray

    class BlockChange(Night):

        Location: Position
        BlockID: VarInt

    class BlockAction(Night):

        Location: Position
        Byte1: UnsignedByte
        Byte2: UnsignedByte
        BlockType: VarInt

    class BlockBreakAnimation(Night):

        EntityID: VarInt
        Location: Position
        DestroyStage: Byte

    class MapChunkBulk(Night):

        SkyLightSent: Bool
        Data: ByteArray

    class Explosion(Night):

        X: Float
        Y: Float
        Z: Float
        Radius: Float
        Data: ByteArray
    
    class Effect(Night):

        EffectID: Int
        Location: Position
        Data: Int
        DisableRelativeVolume: Bool

    class SoundEffect(Night):

        SoundName: String
        EffectPositionX: Int
        EffectPositionY: Int
        EffectPositionZ: Int
        Volume: Float
        Pitch: UnsignedByte

    class Particle(Night):

        ParticleID: Int
        LongDistance: Bool
        X: Float
        Y: Float
        Z: Float
        OffsetX: Float
        OffsetY: Float
        OffsetZ: Float
        ParticleData: Float
        ParticleCount: Int
        Data: ByteArray

    class ChangeGameState(Night):

        Reason: UnsignedByte
        Value: Float
    
    class SpawnGlobalEntity(Night):

        EntityID: VarInt
        Type: Byte
        X: Int
        Y: Int
        Z: Int
    
    class OpenWindow(Night):
        
        WindowID: UnsignedByte
        WindowType: String
        Data: ByteArray
    
    class CloseWindow(Night):

        WindowID: UnsignedByte
    
    class SetSlot(Night):

        WindowID: Byte
        Slot: Short
        SlotData: Slot

    class WindowProperty(Night):

        WindowID: UnsignedByte
        Property: Short
        Value: Short
    
    class ConfirmTransaction(Night):

        WindowID: Byte
        ActionNumber: Short
        Accepted: Bool
    
    class UpdateSign(Night):

        Location: Position
        Lines: ByteArray
    
    class Map(Night):

        MapID: VarInt
        Scale: Byte
        Data: ByteArray

    class UpdateBlockEntity(Night):

        Location: Position
        Action: UnsignedByte
        Data: ByteArray
    
    class OpenSignEditor(Night):

        Location: Position
    
    class Statistics(Night):

        Count: VarInt
        Data: ByteArray

    class PlayerListItem(Night):

        Action: VarInt
        NumberOfPlayers: VarInt
        Data: ByteArray

    class TabComplete(Night):

        Matches: FiniteLengthArray[String]
    
    class ScoreboardObjective(Night):

        ObjectiveName: String
        Mode: Byte
        ObjectiveValue: Optional("Mode", (0, 2))[String]
        Type: Optional("Mode", (0, 2))[String]

    class UpdateScore(Night):

        ScoreName: String
        Action: Byte
        ObjectiveName: String
        Value: Optional("Action", 1, equals=False)[VarInt]
    
    class DisplayScoreboard(Night):

        Position: Byte
        Name: String
    
    class Teams(Night):

        TeamName: String
        Mode: Byte
        TeamDisplayName: Optional("Mode", (0, 2))[String]
        #Data: ByteArray

    class ServerDifficulty(Night):

        Difficulty: UnsignedByte
    
    class CombatEvent(Night):

        Event: VarInt
        Duration: Optional("Event", 1)[VarInt]
        PlayerID: Optional("Event", 2)[VarInt]
        EntityID: Optional("Event", (1, 2))[Int]
        Message: Optional("Event", 2)[String]

    class Camera(Night):

        CameraID: VarInt
    
    class WorldBorder(Night):

        Action: VarInt
        Data: ByteArray
    
    class Title(Night):

        Action: VarInt
        Data: ByteArray

    class SetCompression(Night):

        Threshold: VarInt #warn
    
    class PlayerListHeaderAndFooter(Night):

        Data: ByteArray

    class ResourcePackSend(Night):
        
        URL: String
        Hash: String[[40]]

    class UpdateEntityNBT(Night):

        EntityID: VarInt
        Tag: ByteArray

    map = {
        0x00: KeepAlive,
        0x01: JoinGame,
        0x02: ChatMessage,
        0x03: TimeUpdate,
        0x04: EntityEquipment,
        0x05: SpawnPosition,
        0x06: UpdateHealth,
        0x07: Respawn,
        0x08: PlayerPositionAndLook,
        0x09: HeldItemChange,
        0x0A: UseBed,
        0x0B: Animation,
        0x0C: SpawnPlayer,
        0x0D: CollectItem,
        0x0E: SpawnObject,
        0x0F: SpawnMob,
        0x10: SpawnPainting,
        0x11: SpawnExperienceOrb,
        0x12: EntityVelocity,
        0x13: DestroyEntities,
        0x14: Entity,
        0x15: EntityRelativeMove,
        0x16: EntityLook,
        0x17: EntityLookAndRelativeMove,
        0x18: EntityTeleport,
        0x19: EntityHeadLook,
        0x1A: EntityStatus,
        0x1B: AttachEntity,
        0x1C: EntityMetadata,
        0x1D: EntityEffect,
        0x1E: RemoveEntityEffect,
        0x1F: SetExperience,
        0x20: EntityProperties,
        0x21: ChunkData,
        0x22: MultiBlockChange,
        0x23: BlockChange,
        0x24: BlockAction,
        0x25: BlockBreakAnimation,
        0x26: MapChunkBulk,
        0x27: Explosion,
        0x28: Effect,
        0x29: SoundEffect,
        0x2A: Particle,
        0x2B: ChangeGameState,
        0x2C: SpawnGlobalEntity,
        0x2D: OpenWindow,
        0x2E: CloseWindow,
        0x2F: SetSlot,
        0x30: WindowItems,
        0x31: WindowProperty,
        0x32: ConfirmTransaction,
        0x33: UpdateSign,
        0x34: Map,
        0x35: UpdateBlockEntity,
        0x36: OpenSignEditor,
        0x37: Statistics,
        0x38: PlayerListItem,
        0x39: PlayerAbilities,
        0x3A: TabComplete,
        0x3B: ScoreboardObjective,
        0x3C: UpdateScore,
        0x3D: DisplayScoreboard,
        0x3E: Teams,
        0x3f: PluginMessage,
        0x40: Disconnect,
        0x41: ServerDifficulty,
        0x42: CombatEvent,
        0x43: Camera,
        0x44: WorldBorder,
        0x45: Title,
        0x46: SetCompression,
        0x47: PlayerListHeaderAndFooter,
        0x48: ResourcePackSend,
        0x49: UpdateEntityNBT
    }
    inv_map = {v: k for k, v in map.items()}
